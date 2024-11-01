from enum import Enum


class TransactionsTypes(Enum):
    deposit = "deposit"
    withdraw = "withdraw"
    transfer = "transfer"
