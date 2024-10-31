from uuid import UUID

from pydantic import Field

from src.schemas import BaseSchema


class BankAccountRequest(BaseSchema):
    balance: int = Field(default=0, description="Saldo da conta")


class BankAccountResponse(BaseSchema):
    account_number: int = Field(description="Número da conta")
    balance: int = Field(description="Saldo da conta")
