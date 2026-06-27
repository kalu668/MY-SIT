# Plan: Revamp 'Invest Now' to 'Buy Shares'

## Objective
Replace "Invest Now" terminology and functionality with a broader "Buy Shares" system in the user dashboard, supporting agricultural products, minerals, cryptos, and stocks. This involves backend model updates, admin panel refinement, template renaming, and ensuring seamless deployment to Render.

## Key Files & Context
- `investments/models.py`: Update `Asset` categories and potentially `UserShare` logic.
- `templates/`: Need to find and replace "Invest Now" with "Buy Shares".
- `investments/views.py`: Update views that handle the "Invest" process.
- `investments/admin.py`: Update admin interfaces.

## Implementation Steps

### Phase 1: Backend Refinement
1.  **Modify Models (`investments/models.py`)**:
    *   Update `Asset.CATEGORY_CHOICES` to better reflect the new asset types if needed.
    *   Ensure `Asset` model is robust for Agricultural/Minerals/Stocks/Cryptos.
2.  **Update Views (`investments/views.py`)**:
    *   Rename any "Invest" related views to "Buy Share" related views.
    *   Ensure the buying logic handles different asset types appropriately.

### Phase 2: Admin Panel
1.  **Update `investments/admin.py`**:
    *   Ensure the `AssetAdmin` correctly displays and allows management of the new asset categories.

### Phase 3: Frontend/Templates
1.  **Search & Replace**:
    *   Globally search for "Invest Now" in the `my site` directory.
    *   Replace with "Buy Shares" where appropriate (UI labels, button text, page titles).
2.  **Dashboard Update**:
    *   Update dashboard templates (e.g., `templates/dashboard/`) to reflect "Buy Shares".

### Phase 4: Migration & Deployment
1.  **Migrations**: Run `makemigrations` and `migrate` (if model changes are necessary).
2.  **Testing**: Verify "Buy Shares" flow in a local environment.
3.  **Deployment**: Commit changes and push to GitHub to trigger Render auto-deploy.

## Verification & Testing
- Ensure no "Invest Now" text remains in the UI.
- Verify the "Buy Shares" flow works for all asset categories.
- Ensure admin can still manage all asset types.
- Check Render logs after deployment to ensure no migration/code issues.
