from fastapi import HTTPException, status


class SchemaValueError(HTTPException):
    def __init__(self, detail: str = None) -> None:
        super().__init__(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)
