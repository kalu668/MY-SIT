"""
Investment management utilities
Handles automatic investment status updates and profit calculations
"""
from django.utils import timezone
from django.core.cache import cache
from django.db import transaction
from decimal import Decimal


def check_and_update_investments(user):
    """
    Check and update user's investments when they access the dashboard
    Uses atomic transactions and select_for_update to prevent race conditions
    
    Returns: dict with update statistics
    """
    from investments.models import Investment
    from accounts.models import CustomUser
    
    # Cache key to prevent too frequent updates (soft lock)
    cache_key = f'investment_update_lock_{user.id}'
    if cache.get(cache_key):
        return {'cached': True, 'completed': 0, 'profits_added': Decimal('0')}
    
    # Set soft lock for 30 seconds
    cache.set(cache_key, True, 30)
    
    stats = {
        'completed': 0,
        'profits_added': Decimal('0'),
        'principal_returned': Decimal('0'),
    }
    
    try:
        with transaction.atomic():
            # Lock the user record for update
            locked_user = CustomUser.objects.select_for_update().get(pk=user.id)
            
            # Get all active investments for this user, also locking them
            active_investments = Investment.objects.select_for_update().filter(
                user=locked_user, status='active'
            ).select_related('plan')
            
            for investment in active_investments:
                # Check if investment has matured
                if investment.is_matured():
                    # Calculate any remaining profit
                    days_elapsed = investment.duration_days # Use full duration for matured
                    expected_daily_profit = investment.amount * (investment.plan.daily_roi / Decimal('100'))
                    total_expected = expected_daily_profit * days_elapsed
                    remaining_profit = total_expected - investment.actual_profit
                    
                    if remaining_profit > 0:
                        locked_user.balance += remaining_profit
                        locked_user.total_profit += remaining_profit
                        investment.actual_profit = total_expected
                        stats['profits_added'] += remaining_profit
                    
                    # Return principal amount
                    locked_user.balance += investment.amount
                    locked_user.invested_amount -= investment.amount
                    stats['principal_returned'] += investment.amount
                    
                    # Mark investment as completed
                    investment.status = 'completed'
                    investment.completed_at = timezone.now()
                    investment.save()
                    
                    # Create notification
                    from notifications.models import Notification
                    Notification.objects.create(
                        user=locked_user,
                        title='Investment Completed! 🎉',
                        message=f'Your {investment.plan.name} investment of ${investment.amount} has matured! '
                               f'Total profit earned: ${investment.actual_profit}. '
                               f'Principal amount has been returned to your balance.',
                        notification_type='success'
                    )
                    
                    stats['completed'] += 1
                
                else:
                    # Investment still active - calculate daily profits
                    days_elapsed = investment.days_elapsed
                    expected_daily_profit = investment.amount * (investment.plan.daily_roi / Decimal('100'))
                    expected_profit_so_far = expected_daily_profit * days_elapsed
                    profit_to_add = expected_profit_so_far - investment.actual_profit
                    
                    if profit_to_add > 0:
                        locked_user.balance += profit_to_add
                        locked_user.total_profit += profit_to_add
                        investment.actual_profit = expected_profit_so_far
                        investment.save()
                        stats['profits_added'] += profit_to_add
            
            # Save user changes if any updates were made
            if stats['completed'] > 0 or stats['profits_added'] > 0:
                locked_user.save()
                
                # Refresh original user object balance to match locked_user
                user.balance = locked_user.balance
                user.total_profit = locked_user.total_profit
                user.invested_amount = locked_user.invested_amount
                
    except Exception as e:
        # Clear lock on error so it can be retried
        cache.delete(cache_key)
        raise e
    
    return stats


def calculate_daily_profits_for_user(user):
    """
    Deprecated: Use check_and_update_investments instead for better safety
    """
    return check_and_update_investments(user).get('profits_added', Decimal('0'))
