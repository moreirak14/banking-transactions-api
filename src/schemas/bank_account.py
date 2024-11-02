from datetime import datetime

from pydantic import Field, field_validator

from src.enums.transactions_types import TransactionsTypes
from src.schemas import BaseSchema


class BankAccountRequest(BaseSchema):
    balance: int = Field(default=0, description="Saldo da conta")


class BankAccountResponse(BaseSchema):
    account_number: int = Field(description="Número da conta")
    balance: int = Field(description="Saldo da conta")


class BankAccountTransactionResponse(BaseSchema):
    type: TransactionsTypes = Field(description="Tipo de transação")
    account_number: int = Field(description="Número da conta")
    balance: int = Field(description="Saldo da conta")
    created_at: datetime = Field(description="Data de criação")


class GetBankAccountResponse(BankAccountResponse):
    transactions: list[BankAccountTransactionResponse] | list = Field(
        description="Transações da conta"
    )

    @field_validator("transactions", mode="before")
    def validate_transactions(cls, value: list):
        transactions: list = []

        if not value:
            return transactions

        for transaction in value:
            transaction = BankAccountTransactionResponse(
                type=transaction.type,
                account_number=transaction.account_number,
                balance=transaction.balance,
                created_at=transaction.created_at,
            )
            transactions.append(transaction)

        return transactions
