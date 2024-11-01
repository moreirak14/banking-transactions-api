import pytest
from unittest.mock import AsyncMock, patch

from src.infra.exceptions import SQLAlchemyDatabaseError
from src.schemas.bank_account import BankAccountRequest, BankAccountResponse
from src.services.bank_account import BankAccountService
from src.services.exceptions import InvalidBankAccountDataError


@pytest.fixture
def bank_account_service_mock():
    return BankAccountService()


@pytest.fixture
def bank_account_request_mock():
    return BankAccountRequest(account_number=123456, balance=100)


class TestBankAccountService:
    @pytest.mark.asyncio
    async def test_create_bank_account_success(self, bank_account_service_mock, bank_account_request_mock):
        with patch.object(bank_account_service_mock.repository, 'save', new_callable=AsyncMock) as mock_save, \
                patch.object(bank_account_service_mock.repository, 'get', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = BankAccountResponse(account_number=123456, balance=100)

            response = await bank_account_service_mock.create(bank_account_request_mock)

            mock_save.assert_called_once()
            mock_get.assert_called_once()

            assert response.account_number == 123456
            assert response.balance == 100

    @pytest.mark.asyncio
    async def test_create_bank_account_invalid_data(self, bank_account_service_mock):
        invalid_request = BankAccountRequest(account_number=123456, balance=-100)

        with pytest.raises(InvalidBankAccountDataError):
            await bank_account_service_mock.create(invalid_request)

    @pytest.mark.asyncio
    async def test_create_bank_account_error_database(self, bank_account_service_mock, bank_account_request_mock):
        with patch.object(bank_account_service_mock.repository, 'save', new_callable=AsyncMock), \
                patch.object(bank_account_service_mock.repository, 'get', new_callable=AsyncMock) as mock_get:
            mock_get.side_effect = SQLAlchemyDatabaseError("Gateway Timeout")

            with pytest.raises(SQLAlchemyDatabaseError):
                await bank_account_service_mock.create(bank_account_request_mock)

