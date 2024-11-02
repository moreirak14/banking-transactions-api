from src.adapters.orm.models import BankAccountModel
from src.domains.bank_account import BankAccountDomain
from src.infra.bank_account import BankAccountRepository
from src.schemas.bank_account import (
    BankAccountRequest,
    BankAccountResponse,
    GetBankAccountResponse,
)
from src.services.exceptions import BadRequest, InvalidBankAccountDataError


class BankAccountService:
    def __init__(self):
        self.repository = BankAccountRepository()

    async def create(self, data: BankAccountRequest) -> BankAccountResponse:
        """
        Create a new bank account
        :param data: BankAccountRequest
        :return: BankAccountResponse
        """
        try:
            bank_data_validate = BankAccountDomain(**data.model_dump())
            bank_data: BankAccountModel = bank_data_validate.parse_model()
        except ValueError as error:
            raise InvalidBankAccountDataError(str(error)) from error

        try:
            await self.repository.save(data=bank_data)
            bank_data = await self.repository.get(account_id=bank_data.id)
        except Exception as error:
            raise error from error

        return BankAccountResponse(
            account_number=bank_data.account_number,
            balance=bank_data.balance,
        )

    async def get_by(self, account_number: int) -> GetBankAccountResponse:
        """
        Get bank account by account number
        :param account_number: int
        :return: GetBankAccountResponse
        """
        try:
            bank_data = await self.repository.get_by(
                account_number=account_number
            )
        except Exception as error:
            raise error from error

        if not bank_data:
            raise BadRequest(f"Conta {account_number} não encontrada")

        return GetBankAccountResponse(
            account_number=bank_data.account_number,
            balance=bank_data.balance,
            transactions=bank_data.transactions,
        )
