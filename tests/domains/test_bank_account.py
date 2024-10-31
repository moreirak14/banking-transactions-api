from uuid import UUID

import pytest

from src.domains.bank_account import BankAccountDomain


class TestBankAccountDomain:
    def test_bank_account_must_be_created_with_id_and_as_uuid_by_default(self):
        bank_account = BankAccountDomain()
        assert bank_account.id is not None
        assert isinstance(bank_account.id, UUID)

    def test_created_bank_account_with_default_values(self):
        bank_account = BankAccountDomain()
        assert bank_account.id is not None
        assert isinstance(bank_account.id, UUID)
        assert bank_account.balance == 0

    def test_bank_account_is_created_with_provided_values(self):
        bank_account = BankAccountDomain(balance=100)
        assert bank_account.id is not None
        assert isinstance(bank_account.id, UUID)
        assert bank_account.balance == 100

    def test_bank_account_balance_cant_be_negative(self):
        with pytest.raises(ValueError, match="O saldo da conta não pode ser negativo"):
            BankAccountDomain(balance=-1)

    def test_bank_account_data(self):
        bank_account = BankAccountDomain(balance=100)
        data = bank_account.data()

        assert data.id == bank_account.id
        assert data.balance == bank_account.balance
