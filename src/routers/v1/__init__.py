from fastapi.routing import APIRouter

from src.routers.v1.bank_accounts import bank_accounts_router

router = APIRouter(prefix="/v1")
router.include_router(
    router=bank_accounts_router,
    prefix="/bank_accounts",
    tags=["Contas Bancárias"],
)
