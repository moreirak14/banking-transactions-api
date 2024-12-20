from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from src.adapters.orm.models import BankAccountModel
from src.utils.set_datetime import set_timezone_now

TIMEZONE_NOW: datetime = set_timezone_now()


@dataclass
class BankAccountDomain:
    balance: int = 0
    created_at: str = TIMEZONE_NOW
    updated_at: str = TIMEZONE_NOW

    def __post_init__(self):
        self.validate()

    def validate(self):
        if self.balance < 0:
            raise ValueError("O saldo da conta não pode ser negativo")

    def parse_model(self) -> BankAccountModel:
        _data = BankAccountModel(
            id=uuid4(),
            balance=self.balance,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

        return _data
