from fastapi import FastAPI, Request

from app.core.exceptions import AppException
from app.core.responses import ApiResponse


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(AppException)
    async def app_exception_handler(
        request: Request,
        exc: AppException,
    ):
        return ApiResponse.error(
            exc.message,
            exc.status_code,
        )