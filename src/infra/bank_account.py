from sqlalchemy import Uuid, exists, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from src.adapters.databases import Session
from src.adapters.orm.models import BankAccountModel
from src.infra.exceptions import SQLAlchemyDatabaseError


class BankAccountRepository:
    def __init__(self):
        self.session = Session()

    async def save(self, data: BankAccountModel):
        try:
            with self.session as session:
                session.add(data)
                session.commit()

                return data
        except SQLAlchemyError as error:
            session.rollback()
            raise SQLAlchemyDatabaseError(detail=str(error)) from error
        finally:
            session.close()

    async def get(self, account_id: Uuid) -> BankAccountModel:
        try:
            with self.session as session:
                statement = (
                    select(BankAccountModel)
                    .where(BankAccountModel.id == account_id)
                    .with_for_update()
                )
                account: BankAccountModel = (
                    session.execute(statement).unique().scalar_one_or_none()
                )

                return account
        except SQLAlchemyError as error:
            session.rollback()
            raise SQLAlchemyDatabaseError(detail=str(error)) from error
        finally:
            session.close()

    async def get_by(
        self, account_number: int, for_update: bool = False
    ) -> BankAccountModel | None:
        try:
            with self.session as session:
                bank_account_exists = session.query(
                    exists().where(
                        BankAccountModel.account_number == account_number
                    )
                ).scalar()

                if not bank_account_exists:
                    return None

                if for_update:
                    statement = (
                        select(BankAccountModel)
                        .where(
                            BankAccountModel.account_number == account_number
                        )
                        .with_for_update()
                    )
                else:
                    statement = select(BankAccountModel).where(
                        BankAccountModel.account_number == account_number
                    )

                    statement = statement.options(
                        joinedload(BankAccountModel.transactions)
                    )

                account: BankAccountModel = (
                    session.execute(statement).unique().scalar_one_or_none()
                )

                return account
        except SQLAlchemyError as error:
            session.rollback()
            raise SQLAlchemyDatabaseError(detail=str(error)) from error
        finally:
            session.close()
