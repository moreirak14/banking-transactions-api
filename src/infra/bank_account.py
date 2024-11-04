import logging

from sqlalchemy import Uuid, exists, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from src.adapters.databases import Session
from src.adapters.orm.models import BankAccountModel
from src.infra.exceptions import SQLAlchemyDatabaseError
from src.utils.set_datetime import set_timezone_now

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class BankAccountRepository:
    def __init__(self):
        self.session = Session()

    async def save(self, data: BankAccountModel):
        logger.info("Initializing bank account save...")
        logger.info(f"Saving bank account: {data}")
        try:
            with self.session as session:
                data.updated_at = set_timezone_now()
                session.add(data)
                session.commit()

                return data
        except SQLAlchemyError as error:
            logger.error(f"Error saving bank account: {data}")
            logger.error(f"Error: {error}")
            session.rollback()
            raise SQLAlchemyDatabaseError(detail=str(error)) from error
        finally:
            logger.info(f"Bank account saved: {data}")
            session.close()

    async def get(self, account_id: Uuid) -> BankAccountModel:
        logger.info("Initializing bank account get...")
        logger.info(f"Getting bank account by id: {account_id}")
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
            logger.error(f"Error getting bank account by id: {account_id}")
            logger.error(f"Error: {error}")
            session.rollback()
            raise SQLAlchemyDatabaseError(detail=str(error)) from error
        finally:
            logger.info(f"Bank account found: {account}")
            session.close()

    async def get_by(
        self, account_number: int, for_update: bool = False
    ) -> BankAccountModel | None:
        logger.info("Initializing bank account get by account number...")
        logger.info(
            f"Getting bank account by account number: {account_number}"
        )
        try:
            with self.session as session:
                bank_account_exists = session.query(
                    exists().where(
                        BankAccountModel.account_number == account_number
                    )
                ).scalar()

                if not bank_account_exists:
                    logger.info(f"Bank account not found: {account_number}")
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
            logger.error(
                f"Error getting bank account by account number: {account_number}"  # noqa
            )
            logger.error(f"Error: {error}")
            session.rollback()
            raise SQLAlchemyDatabaseError(detail=str(error)) from error
        finally:
            logger.info(f"Bank account found: {account}")
            session.close()
