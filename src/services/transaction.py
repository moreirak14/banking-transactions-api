from src.adapters.orm.models import BankAccountModel, TransactionModel
from src.domains.transaction import TransactionDomain
from src.infra.bank_account import BankAccountRepository
from src.infra.transaction import TransactionRepository
from src.schemas.transaction import TransactionRequest, TransactionResponse
from src.services.exceptions import BadRequest, InvalidTransactionDataError


class TransactionService:
    def __init__(self):
        self.bank_account_repository = BankAccountRepository()
        self.transaction_repository = TransactionRepository()

    async def create_bank_deposit(self, data: TransactionRequest) -> TransactionResponse:
        """
        Create a bank deposit transaction
        :param data: TransactionRequest
        :return: TransactionResponse
        """
        transaction_data: TransactionModel = await self._check_transaction(data=data)

        bank_data: BankAccountModel = await self._check_and_get_account(account_number=data.account_number)

        transaction_data.bank_account_id = bank_data.id

        transaction_data: TransactionModel = await self._create_transaction(data=transaction_data)

        bank_data.balance += transaction_data.balance

        await self._update_bank_account(data=bank_data)

        return TransactionResponse(
            account_number=bank_data.account_number,
            balance=bank_data.balance,
        )

    async def create_bank_withdraw(self, data: TransactionRequest):
        """
        Create a bank withdraw transaction
        :param data: TransactionRequest
        :return: TransactionResponse
        """
        transaction_data: TransactionModel = await self._check_transaction(data=data)

        bank_data: BankAccountModel = await self._check_and_get_account(account_number=data.account_number)

        if bank_data.balance < transaction_data.balance:
            raise BadRequest("Saldo insuficiente")

        transaction_data.bank_account_id = bank_data.id

        transaction_data: TransactionModel = await self._create_transaction(data=transaction_data)

        bank_data.balance -= transaction_data.balance

        await self._update_bank_account(data=bank_data)

        return TransactionResponse(
            account_number=bank_data.account_number,
            balance=bank_data.balance,
        )


    async def create_bank_transfer(self, data: TransactionRequest):
        """
        Create a bank transfer transaction
        :param data: TransactionRequest
        :return: TransactionResponse
        """
        pass

    @staticmethod
    async def _check_transaction(data: TransactionRequest) -> TransactionModel:
        try:
            transaction_data_validate = TransactionDomain(**data.model_dump())
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
            bank_data: BankAccountModel = await self.bank_account_repository.get_by_account_number(account_number=account_number)
        except Exception as error:
            raise error from error

        if not bank_data:
            raise BadRequest(f"Conta {account_number} não encontrada")

        return bank_data

    async def _create_transaction(self, data: TransactionModel) -> TransactionModel:
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
