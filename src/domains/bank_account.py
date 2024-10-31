from dataclasses import dataclass, field
from uuid import UUID, uuid4

from src.adapters.orm.models import BankAccountModel


@dataclass
class BankAccountDomain:
    id: UUID = field(default_factory=uuid4)
    balance: int = 0

    def __post_init__(self):
        self.validate()

    def validate(self):
        if self.balance < 0:
            raise ValueError("O saldo da conta não pode ser negativo")

    def data(self) -> BankAccountModel:
        _data = BankAccountModel(
            id=self.id,
            balance=self.balance
        )

        return _data
