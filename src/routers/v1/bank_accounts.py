from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer

from src.schemas.bank_account import BankAccountRequest, BankAccountResponse
from src.services.bank_account import BankAccountService

bank_accounts_router = APIRouter(
    dependencies=[Depends(HTTPBearer(auto_error=False))]
)


@bank_accounts_router.post(
    path="",
    description="Criação de conta bancária",
    status_code=status.HTTP_201_CREATED,
    response_model=BankAccountResponse,
)
async def create_bank_accounts(
    data: BankAccountRequest,
) -> BankAccountResponse:
    service = BankAccountService()
    result = await service.create(data=data)

    return result
