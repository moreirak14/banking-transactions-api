from unittest.mock import patch

import pytest
import pytest_asyncio
from starlette.testclient import TestClient

from main import get_app
from src.schemas.bank_account import BankAccountRequest, BankAccountResponse
from src.services.bank_account import BankAccountService


@pytest.fixture()
def client() -> TestClient:
    return TestClient(get_app())


@pytest.fixture
def bank_account_service_mock():
    return BankAccountService()


@pytest.fixture
def bank_account_request_mock():
    return BankAccountRequest(account_number=123456, balance=100)


@pytest_asyncio.fixture
async def create_bank_account_response_mock():
    response = BankAccountResponse(account_number=123456, balance=100)
    mocked = patch.object(
        BankAccountService,
        "create",
        return_value=response,
        autospec=True,
    )
    with mocked as create_bank_account:
        yield create_bank_account
