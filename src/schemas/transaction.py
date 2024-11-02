from typing import Any

from pydantic import Field, field_validator

from src.enums.transactions_types import TransactionsTypes
from src.schemas import BaseSchema
from src.schemas.exceptions import SchemaValueError


class TransactionDepositRequest(BaseSchema):
    type: str = Field(
        default=TransactionsTypes.deposit.value,
        description="Tipo de transação",
    )
    account_number: int = Field(description="Número da conta")
    balance: int = Field(default=0, description="Saldo da conta")

    @field_validator("type", mode="before")
    def validate_type(cls, value: Any):
        try:
            if value != TransactionsTypes.deposit.value:
                raise SchemaValueError(
                    "Tipo de transação inválido",
                )
            return value
        except ValueError as error:
            raise error from error


class TransactionWithdrawRequest(BaseSchema):
    type: str = Field(
        default=TransactionsTypes.withdraw.value,
        description="Tipo de transação",
    )
    account_number: int = Field(description="Número da conta")
    balance: int = Field(default=0, description="Saldo da conta")

    @field_validator("type", mode="before")
    def validate_type(cls, value: Any):
        try:
            if value != TransactionsTypes.withdraw.value:
                raise SchemaValueError(
                    "Tipo de transação inválido",
                )
            return value
        except ValueError as error:
            raise error from error


class TransactionTransferRequest(BaseSchema):
    type: str = Field(
        default=TransactionsTypes.transfer.value,
        description="Tipo de transação",
    )
    account_number: int = Field(description="Número da conta")
    balance: int = Field(default=0, description="Saldo da conta")

    @field_validator("type", mode="before")
    def validate_type(cls, value: Any):
        try:
            if value != TransactionsTypes.transfer.value:
                raise SchemaValueError(
                    "Tipo de transação inválido",
                )
            return value
        except ValueError as error:
            raise error from error


class TransactionResponse(BaseSchema):
    account_number: int = Field(description="Número da conta")
    balance: int = Field(description="Saldo da conta")
