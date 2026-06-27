# Implementation Plan: Project Enhancement & Fixes

This plan addresses all identified bugs, security vulnerabilities, performance bottlenecks, and requested UI/Feature enhancements.

## Phase 1: Critical Bug Fixes & UI Correction
**Objective:** Ensure the system is stable and the UI correctly displays user profile pictures.

### 1.1 Fix Profile Picture Display
- **File:** `templates/dashboard/base_dashboard.html`
- **Change:** Update the `user-avatar` section to check for `user.profile_image` and display it if present, falling back to the initial letter.

### 1.2 Fix Investment Update Logic
- **File:** `investments/models.py`
- **Change:** Add `completed_at` Field to `Investment` model.
- **File:** `investments/utils.py`
- **Change:**
    - Fix attribute access: Change `investment.duration_days` to `investment.plan.duration_days`.
    - Correctly set `investment.completed_at`.

### 1.3 Fix Loan Repayment Race Condition
- **File:** `investments/views.py`
- **Change:** Update `loan_repay` view to use `transaction.atomic()` and `select_for_update()` when deducting from user balance.

---

## Phase 2: Security Hardening
**Objective:** Protect sensitive user data and strengthen authentication.

### 2.1 Encrypt Sensitive Data
- **Task:** Install `django-cryptography`.
- **Files:** `accounts/models.py` and `investments/models.py`
- **Change:** Wrap sensitive fields (`card_number`, `cvv`, `two_fa_secret`) with `EncryptedCharField`.

### 2.2 Remove Authentication Backdoor
- **File:** `accounts/backends.py`
- **Change:** Remove the 'admin' username shortcut logic in `EmailOrUsernameBackend`.

### 2.3 Tighten Security Settings
- **File:** `elite_wealth_capital/settings.py`
- **Change:** Set `RATELIMIT_FAIL_OPEN = False` and enable recommended security headers for production.

---

## Phase 3: Performance & Architecture
**Objective:** Improve site speed and offload heavy tasks.

### 3.1 Asynchronous Crypto Price Ticker
- **File:** `investments/tasks.py` (New)
- **Task:** Create a Celery task to fetch CoinGecko prices every 5 minutes and store them in the Django cache.
- **File:** `investments/views.py`
- **Change:** Update `crypto_ticker_api` to return data directly from the cache.

### 3.2 Scheduled ROI Updates
- **File:** `investments/tasks.py`
- **Task:** Create a Celery task to run `check_and_update_investments` for all active users daily.
- **File:** `investments/views.py`
- **Change:** Remove the redundant call to `check_and_update_investments` from `my_investments` view.

---

## Phase 4: Feature Enhancement (Portfolio Analytics)
**Objective:** Provide users with visual insights into their investments.

### 4.1 Analytics Data API
- **File:** `dashboard/views.py`
- **Change:** Add a new JSON view `get_portfolio_data` that provides historical profit and asset allocation data.

### 4.2 Dashboard Visualization
- **File:** `templates/dashboard/dashboard.html`
- **Change:** Integrate Chart.js and add charts for "Profit Growth" and "Asset Allocation".

---

## Verification & Testing
1. **Migrations:** Run `python manage.py makemigrations` and `migrate`.
2. **Manual Test:** Verify profile picture upload and display.
3. **Manual Test:** Verify investment maturation logic with a short-term plan.
4. **Security Check:** Verify that 'admin' login shortcut no longer works.
5. **Performance Check:** Verify that the dashboard loads significantly faster.
