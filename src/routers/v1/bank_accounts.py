from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer

from src.schemas.bank_account import (
    BankAccountRequest,
    BankAccountResponse,
    GetBankAccountResponse,
)
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


@bank_accounts_router.get(
    path="/{account_number:int}",
    description="Busca de conta bancária",
    status_code=status.HTTP_200_OK,
    response_model=GetBankAccountResponse,
)
async def get_bank_accounts(
    account_number: int,
) -> GetBankAccountResponse:
    service = BankAccountService()
    result = await service.get_by(account_number=account_number)

    return result
