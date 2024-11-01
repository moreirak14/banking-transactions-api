from sqlalchemy import Uuid, select
from sqlalchemy.exc import SQLAlchemyError

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
