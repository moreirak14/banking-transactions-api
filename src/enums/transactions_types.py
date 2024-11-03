from enum import Enum


class TransactionsTypes(Enum):
    deposit = "deposit"
    withdraw = "withdraw"
    transfer = "transfer"
    transfer_sent = "transfer_sent"
    transfer_received = "transfer_received"
