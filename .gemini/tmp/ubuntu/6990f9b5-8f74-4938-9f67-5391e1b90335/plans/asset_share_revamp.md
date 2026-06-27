# Plan: Asset Share-Based Model Revamp

## Objective
Transform the existing investment system into a comprehensive share-based asset platform supporting Agriculture, Oil, Minerals, Crypto, and Stocks. Replace "Invest Now" with "Buy Shares".

## Scope & Impact
- **Models**: Redefine assets and user holdings.
- **Backend**: Update purchase logic, asset tracking, and wallet deductions.
- **Frontend**: Revamp "Buy Shares" UI, Dashboard asset display, and portfolio management.
- **Admin**: Manage asset pricing, categories, and user holdings.

## Proposed Changes

### 1. Data Model (`investments/models.py`)
- Create `AssetType` (Agriculture, Oil, Minerals, Crypto, Stocks).
- Create `Asset` model (name, ticker, category, price_per_share, description, image).
- Create `UserShare` model (user, asset, quantity, purchase_price, purchase_date).
- Refactor `Investment` model to be a `SharePurchase` record.

### 2. Backend Logic (`investments/views.py`)
- Replace `withdraw_view` and `invest_view` with `buy_shares_view`.
- Implement dynamic price calculation and portfolio update on purchase.

### 3. Frontend Revamp (`templates/investments/buy_shares.html`)
- Modern, clean UI showing asset details, current price per share, and interactive purchase calculator.

### 4. Admin Panel (`investments/admin.py`)
- Add `AssetAdmin` for creating/managing available assets.
- Add `UserShareAdmin` for managing user holdings.

## Implementation Steps
1.  **Draft Models & Admin**: Create the new structure.
2.  **User Consent**: Review the planned model structure.
3.  **Backend Migration**: Write logic to handle share purchases and database migrations.
4.  **UI/UX Revamp**: Build new templates for asset purchasing.
5.  **Integration**: Update dashboard to show user's share portfolio instead of "investments".
6.  **Testing & Deployment**: Validate, then commit and push to Render.

## Alternatives Considered
- Keeping the existing `InvestmentPlan` model, but it lacks the flexibility to handle assets with fluctuating share prices and distinct categories. A dedicated asset model is required.
