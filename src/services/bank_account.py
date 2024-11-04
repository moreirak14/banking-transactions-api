import logging

from src.adapters.orm.models import BankAccountModel
from src.domains.bank_account import BankAccountDomain
from src.infra.bank_account import BankAccountRepository
from src.schemas.bank_account import (
    BankAccountRequest,
    BankAccountResponse,
    GetBankAccountResponse,
)
from src.services.exceptions import BadRequest, InvalidBankAccountDataError

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class BankAccountService:
    def __init__(self):
        self.repository = BankAccountRepository()

    async def create(self, data: BankAccountRequest) -> BankAccountResponse:
        """
        Create a new bank account
        :param data: BankAccountRequest
        :return: BankAccountResponse
        """
        logger.info(f"Creating bank account: {data}")
        try:
            bank_data_validate = BankAccountDomain(**data.model_dump())
            bank_data: BankAccountModel = bank_data_validate.parse_model()
        except ValueError as error:
            logger.error(f"Invalid bank account data: {data}")
            logger.error(f"Error: {error}")
            raise InvalidBankAccountDataError(str(error)) from error

        try:
            await self.repository.save(data=bank_data)
            bank_data = await self.repository.get(account_id=bank_data.id)
        except Exception as error:
            logger.error(f"Error creating bank account: {data}")
            logger.error(f"Error: {error}")
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
        logger.info(
            f"Getting bank account by account number: {account_number}"
        )
        try:
            bank_data = await self.repository.get_by(
                account_number=account_number
            )
            logger.info(f"Bank account found: {bank_data}")
        except Exception as error:
            logger.error(
                f"Error getting bank account by account number: {account_number}"  # noqa
            )
            logger.error(f"Error: {error}")
            raise error from error

        if not bank_data:
            logger.error(f"Bank account not found: {account_number}")
            raise BadRequest(f"Conta {account_number} não encontrada")

        return GetBankAccountResponse(
            account_number=bank_data.account_number,
            balance=bank_data.balance,
            transactions=bank_data.transactions,
        )
