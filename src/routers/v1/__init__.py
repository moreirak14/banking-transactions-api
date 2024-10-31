from fastapi.routing import APIRouter

from src.routers.v1.bank_account import bank_account_router

router = APIRouter(prefix="/v1")
router.include_router(
    router=bank_account_router, prefix="/bank_accounts", tags=["Contas Bancárias"]
)
