from fastapi import HTTPException, status


class SQLAlchemyDatabaseError(HTTPException):
    def __init__(self, detail: str = None) -> None:
        super().__init__(status.HTTP_503_SERVICE_UNAVAILABLE, detail=detail)
