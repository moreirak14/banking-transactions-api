from typing import Any
from uuid import uuid4

from src.adapters.orm.models import BankAccountModel, TransactionModel
from src.domains.transaction import TransactionDomain
from src.enums.transactions_types import TransactionsTypes
from src.infra.bank_account import BankAccountRepository
from src.infra.transaction import TransactionRepository
from src.schemas.transaction import (
    TransactionDepositRequest,
    TransactionResponse,
    TransactionTransferRequest,
    TransactionTransferResponse,
    TransactionWithdrawRequest,
)
from src.services.exceptions import BadRequest, InvalidTransactionDataError
from src.utils.set_datetime import set_timezone_now


class TransactionService:
    def __init__(self):
        self.bank_account_repository = BankAccountRepository()
        self.transaction_repository = TransactionRepository()

    async def create_bank_deposit(
        self, data: TransactionDepositRequest
    ) -> TransactionResponse:
        """
        Create a bank deposit transaction
        :param data: TransactionRequest
        :return: TransactionResponse
        """
        transaction_data: TransactionModel = await self._check_transaction(
            type=TransactionsTypes(data.type), data=data
        )

        bank_data: BankAccountModel = await self._check_and_get_account(
            account_number=data.account_number
        )

        transaction_data.bank_account_id = bank_data.id

        transaction_data: TransactionModel = await self._create_transaction(
            data=transaction_data
        )

        bank_data.balance += transaction_data.balance

        await self._update_bank_account(data=bank_data)

        return TransactionResponse(
            account_number=bank_data.account_number,
            balance=bank_data.balance,
        )

    async def create_bank_withdraw(self, data: TransactionWithdrawRequest):
        """
        Create a bank withdraw transaction
        :param data: TransactionRequest
        :return: TransactionResponse
        """
        transaction_data: TransactionModel = await self._check_transaction(
            type=TransactionsTypes(data.type), data=data
        )

        bank_data: BankAccountModel = await self._check_and_get_account(
            account_number=data.account_number
        )

        if bank_data.balance < transaction_data.balance:
            raise BadRequest("Saldo insuficiente")

        transaction_data.bank_account_id = bank_data.id

        transaction_data: TransactionModel = await self._create_transaction(
            data=transaction_data
        )

        bank_data.balance -= transaction_data.balance

        await self._update_bank_account(data=bank_data)

        return TransactionResponse(
            account_number=bank_data.account_number,
            balance=bank_data.balance,
        )

    async def create_bank_transfer(
        self, data: TransactionTransferRequest
    ) -> TransactionTransferResponse:
        """
        Create a bank transfer transaction
        :param data: TransactionTransferRequest
        :return: TransactionResponse
        """
        from_account_data: TransactionModel = await self._check_transaction(
            type=TransactionsTypes.TRANSFER_SENT, data=data.from_account
        )

        from_account_bank_data: BankAccountModel = (
            await self._check_and_get_account(
                account_number=data.from_account.account_number
            )
        )

        if from_account_bank_data.balance < from_account_data.balance:
            raise BadRequest("Saldo insuficiente")

        from_account_data.bank_account_id = from_account_bank_data.id

        to_account_data: TransactionModel = TransactionModel(
            id=uuid4(),
            type=TransactionsTypes.TRANSFER_RECEIVED,
            account_number=data.to_account,
            balance=from_account_data.balance,
            created_at=set_timezone_now(),
        )

        to_account_bank_data: BankAccountModel = (
            await self._check_and_get_account(
                account_number=to_account_data.account_number
            )
        )

        from_account_data: TransactionModel = await self._create_transaction(
            data=from_account_data
        )

        to_account_data.bank_account_id = to_account_bank_data.id

        await self._create_transaction(data=to_account_data)

        to_account_bank_data.balance += from_account_data.balance

        from_account_bank_data.balance -= from_account_data.balance

        await self._update_bank_account(data=from_account_bank_data)

        await self._update_bank_account(data=to_account_bank_data)

        return TransactionTransferResponse(
            from_account=TransactionResponse(
                account_number=from_account_bank_data.account_number,
                balance=from_account_bank_data.balance,
            ),
            to_account=TransactionResponse(
                account_number=to_account_bank_data.account_number,
                balance=to_account_bank_data.balance,
            ),
        )

    @staticmethod
    async def _check_transaction(
        type: TransactionsTypes,
        data: Any,
    ) -> TransactionModel:
        try:
            transaction_data_validate = TransactionDomain(
                type=type,
                account_number=data.account_number,
                balance=data.balance,
            )
            return transaction_data_validate.parse_model()
        except ValueError as error:
            raise InvalidTransactionDataError(str(error)) from error

    async def _check_and_get_account(self, account_number: int):
        """
        Check if account exists and return it
        :param account_number: int
        :return: BankAccountModel
        """
        try:
            bank_data: BankAccountModel = (
                await self.bank_account_repository.get_by(
                    account_number=account_number, for_update=True
                )
            )
        except Exception as error:
            raise error from error

        if not bank_data:
            raise BadRequest(f"Conta {account_number} não encontrada")

        return bank_data

    async def _create_transaction(
        self, data: TransactionModel
    ) -> TransactionModel:
        try:
            transaction_data = await self.transaction_repository.save(data)
            return transaction_data
        except Exception as error:
            raise error from error

    async def _update_bank_account(self, data: BankAccountModel):
        try:
            await self.bank_account_repository.save(data)
        except Exception as error:
            raise error from error
