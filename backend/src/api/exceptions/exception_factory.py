from fastapi import HTTPException


class HttpExceptionFactory:
    @staticmethod
    def create_http_exception(
            status_code: int,
            detail: str
    ) -> HTTPException:
        raise HTTPException(status_code=status_code,detail=detail)