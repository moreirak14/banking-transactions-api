import logging

from sqlalchemy.exc import SQLAlchemyError

from src.adapters.databases import Session
from src.adapters.orm.models import TransactionModel
from src.infra.exceptions import SQLAlchemyDatabaseError

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TransactionRepository:
    def __init__(self):
        self.session = Session()

    async def save(self, data: TransactionModel) -> TransactionModel:
        logger.info("Initializing transaction save...")
        logger.info(f"Saving transaction: {data}")
        try:
            with self.session as session:
                session.add(data)
                session.commit()

                return data
        except SQLAlchemyError as error:
            logger.error(f"Error saving transaction: {data}")
            logger.error(f"Error: {error}")
            session.rollback()
            raise SQLAlchemyDatabaseError(detail=str(error)) from error
        finally:
            logger.info(f"Transaction saved: {data}")
            session.close()
