from typing import Any

from pydantic import Field, field_validator

from src.enums.transactions_types import TransactionsTypes
from src.schemas import BaseSchema
from src.schemas.exceptions import SchemaValueError


class BaseTransactionRequest(BaseSchema):
    account_number: int = Field(description="Número da conta")
    balance: int = Field(default=0, description="Saldo da conta")


class TransactionResponse(BaseSchema):
    account_number: int = Field(description="Número da conta")
    balance: int = Field(description="Saldo da conta")


class TransactionDepositRequest(BaseTransactionRequest):
    type: str = Field(
        default=TransactionsTypes.DEPOSIT.value,
        description="Tipo de transação",
    )

    @field_validator("type", mode="before")
    def validate_type(cls, value: Any):
        try:
            if value != TransactionsTypes.DEPOSIT.value:
                raise SchemaValueError(
                    "Tipo de transação inválido",
                )
            return value
        except ValueError as error:
            raise error from error


class TransactionWithdrawRequest(BaseTransactionRequest):
    type: str = Field(
        default=TransactionsTypes.WITHDRAW.value,
        description="Tipo de transação",
    )

    @field_validator("type", mode="before")
    def validate_type(cls, value: Any):
        try:
            if value != TransactionsTypes.WITHDRAW.value:
                raise SchemaValueError(
                    "Tipo de transação inválido",
                )
            return value
        except ValueError as error:
            raise error from error


class TransactionTransferRequest(BaseSchema):
    type: str = Field(
        default=TransactionsTypes.TRANSFER.value,
        description="Tipo de transação",
    )
    from_account: BaseTransactionRequest = Field(
        description="Conta de origem da transferência",
    )
    to_account: int = Field(
        description="Conta de destino da transferência",
    )

    @field_validator("type", mode="before")
    def validate_type(cls, value: Any):
        try:
            if value != TransactionsTypes.TRANSFER.value:
                raise SchemaValueError(
                    "Tipo de transação inválido",
                )
            return value
        except ValueError as error:
            raise error from error


class TransactionTransferResponse(BaseSchema):
    from_account: TransactionResponse = Field(
        description="Conta de origem da transferência",
    )
    to_account: TransactionResponse = Field(
        description="Conta de destino da transferência",
    )
