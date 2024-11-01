from src.adapters.orm.models import BankAccountModel
from src.domains.bank_account import BankAccountDomain
from src.infra.bank_account import BankAccountRepository
from src.schemas.bank_account import BankAccountRequest, BankAccountResponse
from src.services.exceptions import InvalidBankAccountDataError


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
