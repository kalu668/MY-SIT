import os
import django
import sys
from decimal import Decimal
from django.apps import apps

# Setup Django environment
sys.path.append('/home/ubuntu/my site')
from pathlib import Path
BASE_DIR = Path('/home/ubuntu/my site')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elite_wealth_capital.settings')
print("Setting up Django...")
# Force settings to use the correct database
from django.conf import settings
settings.DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
}
django.setup()
print("Django setup complete.")

def check_user_balance(email):
    CustomUser = apps.get_model('accounts', 'CustomUser')
    try:
        user = CustomUser.objects.get(email=email)
        print(f"User: {user.email}")
        print(f"Balance: {user.balance}")
        print(f"Invested Amount: {user.invested_amount}")
        print(f"Total Profit: {user.total_profit}")
    except CustomUser.DoesNotExist:
        print(f"User with email {email} not found.")

if __name__ == '__main__':
    CustomUser = apps.get_model('accounts', 'CustomUser')
    users = CustomUser.objects.all()
    print(f"Total users: {users.count()}")
    for user in users[:5]:
        print(f"{user.email}: Balance={user.balance}")
