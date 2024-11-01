from sqlalchemy.exc import SQLAlchemyError

from src.adapters.databases import Session
from src.adapters.orm.models import TransactionModel
from src.infra.exceptions import SQLAlchemyDatabaseError


class TransactionRepository:
    def __init__(self):
        self.session = Session()

    async def save(self, data: TransactionModel) -> TransactionModel:
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
