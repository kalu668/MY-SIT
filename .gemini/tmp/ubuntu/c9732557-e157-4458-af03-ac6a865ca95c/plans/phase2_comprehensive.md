# Implementation Plan: Phase 2 - Advanced Features & Refactoring

This phase focuses on enhancing system reliability, security, and user experience through automation, real-time features, and code quality improvements.

## 1. Fix "Buy Shares" & Mobile Optimization
**Objective:** Resolve persistent errors in the share purchase flow and ensure a seamless experience on all devices.

### 1.1 "Buy Shares" Fix
- **File:** `investments/views.py`
- **Changes:**
    - Improve error logging in `create_investment` to capture specific failure points.
    - Ensure `request.user.balance` is refreshed from the database before any checks.
    - Add descriptive error messages for different failure scenarios (e.g., plan expired, limit reached).
- **File:** `templates/investments/plans.html` & `templates/investments/invest.html`
- **Changes:**
    - Redesign layout to be "line-by-line" (list view) instead of large cards, as requested.
    - Ensure all form elements and buttons are touch-friendly and fully responsive.

---

## 2. Real-time Notifications (Django Channels)
**Objective:** Notify users instantly of balance updates and investment completions.

### 2.1 WebSocket Integration
- **Infrastructure:** Set up Django Channels with Redis as the layer.
- **Backend:** Create a notification consumer to push updates to specific user groups.
- **Frontend:** Add a lightweight WebSocket client to the dashboard to receive and display toast notifications.

---

## 3. PDF Generation (Investment Receipts)
**Objective:** Provide users with professional proof of their investments.

### 3.1 PDF Generator
- **Library:** Use `reportlab` (already in requirements).
- **Backend:** Create a view to generate a PDF receipt for any successful investment.
- **Receipt Details:** User info, plan name, amount, ROI details, and timestamp.
- **UI:** Add a "Download Receipt" button to the `my_investments` page.

---

## 4. Automated Testing
**Objective:** Prevent regressions in critical financial logic.

### 4.1 Test Suite
- **Scope:** 
    - Unit tests for `investments/tasks.py` (ROI calculations).
    - Integration tests for `create_investment`, `deposit_view`, and `withdraw_view`.
    - Edge case testing for balance race conditions.

---

## 5. Automated Database Backups
**Objective:** Ensure data safety with scheduled backups.

### 5.1 Backup Task
- **File:** `tasks/tasks.py` (New or existing)
- **Task:** Create a Celery task that performs a database dump and stores it securely (local or cloud).
- **Schedule:** Set to run daily via `django-celery-beat`.

---

## 6. Code Refactoring
**Objective:** Improve maintainability by reducing file complexity.

### 6.1 Modularization
- Split `investments/views.py` into:
    - `views_investments.py`
    - `views_banking.py` (deposits/withdrawals)
    - `views_cards.py`
- Standardize error handling and logging across all modules.

---

## Verification & Testing
1. **Manual:** Test the "Buy Shares" flow on mobile and desktop.
2. **Automated:** Run the new test suite (`python manage.py test`).
3. **Receipt Check:** Verify generated PDF formatting and accuracy.
4. **Real-time Check:** Verify notification popups during transactions.
