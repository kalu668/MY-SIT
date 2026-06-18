// Real-time Notification System
const notificationSound = new Audio('/static/sounds/notification.mp3');

function showNotificationToast(notification) {
    const toastEl = document.getElementById('notificationToast');
    if (!toastEl) return;

    const toastMessage = document.getElementById('toastMessage');
    const toastAction = document.getElementById('toastAction');
    const toastTime = document.getElementById('toastTime');

    if (toastMessage) toastMessage.textContent = notification.message || 'You have a new message';
    if (toastAction) {
        toastAction.href = notification.action_url || '/notifications/';
        if (notification.action_url) {
            toastAction.style.display = 'block';
        } else {
            toastAction.style.display = 'none';
        }
    }
    if (toastTime) toastTime.textContent = 'Just now';

    const toast = new bootstrap.Toast(toastEl, { delay: 10000 });
    toast.show();

    // Play sound
    notificationSound.play().catch(e => console.log('Autoplay prevented or sound file missing'));
}

function checkNotifications() {
    fetch('/notifications/check/')
        .then(response => response.json())
        .then(data => {
            if (data.new_notifications) {
                // Fetch the most recent notification to display in toast
                fetch('/notifications/recent/')
                    .then(res => res.json())
                    .then(recentData => {
                        if (recentData.notifications && recentData.notifications.length > 0) {
                            showNotificationToast(recentData.notifications[0]);
                        }
                    });
                
                // Update any notification count badges on the page
                updateNotificationBadges(data.count);
            }
        })
        .catch(err => console.error('Error checking notifications:', err));
}

function updateNotificationBadges(count) {
    const badges = document.querySelectorAll('.notification-badge, .unread-count-badge');
    badges.forEach(badge => {
        badge.textContent = count;
        if (count > 0) {
            badge.style.display = 'inline-block';
        } else {
            badge.style.display = 'none';
        }
    });
}

// Poll every 30 seconds for new notifications
// Only start polling if user is logged in (handled by endpoint returning 403 otherwise)
setInterval(checkNotifications, 30000);

// Initial check on load
document.addEventListener('DOMContentLoaded', () => {
    // Small delay to ensure all JS is loaded
    setTimeout(checkNotifications, 2000);
});
