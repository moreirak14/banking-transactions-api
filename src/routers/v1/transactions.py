from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer

from src.schemas.transaction import TransactionResponse, TransactionRequest
from src.services.transaction import TransactionService

transactions_router = APIRouter(
    dependencies=[Depends(HTTPBearer(auto_error=False))]
)


@transactions_router.post(
    path="/bank-deposits",
    description="Criação de depósito bancário",
    status_code=status.HTTP_201_CREATED,
    response_model=TransactionResponse,
)
async def create_bank_deposits(
    data: TransactionRequest,
) -> TransactionResponse:
    service = TransactionService()
    result = await service.create_bank_deposit(data)

    return result


@transactions_router.post(
    path="/bank-withdraws",
    description="Criação de saque bancário",
    status_code=status.HTTP_201_CREATED,
    response_model=TransactionResponse,
)
async def create_bank_withdraws(
    data: TransactionRequest,
) -> TransactionResponse:
    service = TransactionService()
    result = await service.create_bank_withdraw(data)

    return result
