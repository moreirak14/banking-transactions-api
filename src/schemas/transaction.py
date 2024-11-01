from typing import Any

from pydantic import Field, field_validator

from src.enums.transactions_types import TransactionsTypes
from src.schemas import BaseSchema
from src.schemas.exceptions import SchemaValueError


class TransactionRequest(BaseSchema):
    type: TransactionsTypes = Field(description="Tipo de transação")
    account_number: int = Field(description="Número da conta")
    balance: int = Field(default=0, description="Saldo da conta")

    @field_validator("type", mode="before")
    def validate_type(cls, value: Any):
        try:
            return TransactionsTypes(value).value
        except ValueError as error:
            raise SchemaValueError(
                "Tipo de transação inválido",
            ) from error


class TransactionResponse(BaseSchema):
    account_number: int = Field(description="Número da conta")
    balance: int = Field(description="Saldo da conta")
