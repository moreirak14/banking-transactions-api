from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from src.adapters.orm.models import TransactionModel
from src.enums.transactions_types import TransactionsTypes
from src.utils.set_datetime import set_timezone_now

TIMEZONE_NOW: datetime = set_timezone_now()


@dataclass
class TransactionDomain:
    type: TransactionsTypes
    account_number: int
    balance: int = 0
    created_at: str = TIMEZONE_NOW

    def __post_init__(self):
        self.validate()

    def validate(self):
        if self.balance <= 0:
            raise ValueError(
                "O valor da transação não pode ser negativo ou zero"
            )

    def parse_model(self) -> TransactionModel:
        _data = TransactionModel(
            id=uuid4(),
            type=self.type,
            account_number=self.account_number,
            balance=self.balance,
            created_at=self.created_at,
        )

        return _data
