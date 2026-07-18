from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    ResourceNotFoundError,
    DuplicateResourceError,
    BusinessValidationError,
)


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(ResourceNotFoundError)
    async def resource_not_found_handler(
        request: Request,
        exc: ResourceNotFoundError,
    ):
        return JSONResponse(
            status_code=404,
            content={
                "detail": exc.message
            },
        )

    @app.exception_handler(DuplicateResourceError)
    async def duplicate_resource_handler(
        request: Request,
        exc: DuplicateResourceError,
    ):
        return JSONResponse(
            status_code=409,
            content={
                "detail": exc.message
            },
        )

    @app.exception_handler(BusinessValidationError)
    async def validation_handler(
        request: Request,
        exc: BusinessValidationError,
    ):
        return JSONResponse(
            status_code=400,
            content={
                "detail": exc.message
            },
        )