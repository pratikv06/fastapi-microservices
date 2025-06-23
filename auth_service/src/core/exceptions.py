# third party
from src.utils.response_format import APIResponse

# fastapi
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse


async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=APIResponse(
            status=exc.status_code,
            message="Error occurred while processing the request ;(",
            error=exc.detail,
        ).model_dump(),
    )
