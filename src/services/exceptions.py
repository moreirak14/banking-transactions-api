from fastapi import HTTPException, status


class BadRequest(HTTPException):
    def __init__(self, detail: str = None) -> None:
        super().__init__(status.HTTP_400_BAD_REQUEST, detail=detail)


class InvalidBankAccountDataError(BadRequest):
    def __init__(self, detail: str = None) -> None:
        super().__init__(detail=detail)


class InvalidTransactionDataError(BadRequest):
    def __init__(self, detail: str = None) -> None:
        super().__init__(detail=detail)
