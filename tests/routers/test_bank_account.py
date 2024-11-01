import pytest
from fastapi import status


class TestBankAccountRouter:
    @pytest.mark.asyncio
    async def test_create_bank_account(self, client, create_bank_account_response_mock):
        payload: dict = {
            "balance": 100
        }
        response = client.post(url="/v1/bank_accounts", json=payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {
            "account_number": 123456,
            "balance": 100
        }
