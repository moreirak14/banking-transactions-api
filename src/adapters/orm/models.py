from sqlalchemy import MetaData, Uuid, Integer, Sequence
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


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
