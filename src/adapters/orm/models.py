from datetime import datetime

from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    MetaData,
    Sequence,
    Uuid,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.enums.transactions_types import TransactionsTypes


class Base(DeclarativeBase):
    metadata = MetaData()


class BankAccountModel(Base):
    __tablename__ = "bank_accounts"

    id: Mapped[Uuid] = mapped_column(
        Uuid, primary_key=True, unique=True, nullable=False
    )
    account_number: Mapped[int] = mapped_column(
        Integer,
        Sequence(name="account_number_seq", start=1),
        unique=True,
        nullable=False,
    )
    balance: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    transactions: Mapped[list["TransactionModel"]] = relationship(
        back_populates="bank_account"
    )


class TransactionModel(Base):
    __tablename__ = "transactions"

    id: Mapped[Uuid] = mapped_column(
        Uuid, primary_key=True, unique=True, nullable=False
    )
    bank_account_id: Mapped[Uuid] = mapped_column(
        ForeignKey("bank_accounts.id"), nullable=False
    )
    bank_account: Mapped["BankAccountModel"] = relationship(
        back_populates="transactions"
    )
    type: Mapped[str] = mapped_column(Enum(TransactionsTypes), nullable=False)
    account_number: Mapped[int] = mapped_column(Integer, nullable=False)
    balance: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
