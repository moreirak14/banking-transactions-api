from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy import Uuid
from sqlalchemy.exc import SQLAlchemyError

from src.adapters.orm.models import BankAccountModel
from src.infra.bank_account import BankAccountRepository
from src.infra.exceptions import SQLAlchemyDatabaseError


class TestBankAccountRepository:
    @pytest.mark.asyncio
    async def test_save_success(self):
        repo = BankAccountRepository()
        data = BankAccountModel(id=Uuid(), balance=100)

        with patch.object(repo, "session", MagicMock()) as mock_session:
            mock_session.__enter__.return_value = mock_session
            mock_session.add.return_value = None
            mock_session.commit.return_value = None

            result = await repo.save(data)

            mock_session.add.assert_called_once_with(data)
            mock_session.commit.assert_called_once()
            assert result == data

    @pytest.mark.asyncio
    async def test_save_failure(self):
        repo = BankAccountRepository()
        data = BankAccountModel(id=Uuid(), balance=100)

        with patch.object(repo, "session", MagicMock()) as mock_session:
            mock_session.__enter__.return_value = mock_session
            mock_session.add.side_effect = SQLAlchemyError

            with pytest.raises(SQLAlchemyDatabaseError):
                await repo.save(data)

            mock_session.rollback.assert_called_once()
            mock_session.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_success(self):
        repo = BankAccountRepository()
        account_id = Uuid()
        account = BankAccountModel(id=account_id, balance=100)

        with patch.object(repo, "session", MagicMock()) as mock_session:
            mock_session.__enter__.return_value = mock_session
            mock_session.execute.return_value.unique.return_value.scalar_one_or_none.return_value = account  # noqa

            result = await repo.get(account_id)

            assert result == account
