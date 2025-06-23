# stdlib
import time

# third party
from src.core.logger import logger
from starlette.middleware.base import BaseHTTPMiddleware

# fastapi
from fastapi import Request


class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """
        Middleware to log HTTP request/response details.
        Args:
            request (Request): The incoming HTTP request
            call_next: The next middleware/route handler in the chain
        Returns:
            Response: The HTTP response from downstream handlers
        Logs:
            - Request method (GET, POST, PUT, DELETE etc)
            - Request URL path
            - Request query parameters
            - Request payload/body
            - Response status code
            - Response time duration in seconds
        """
        payload = await request.body()

        start_time = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start_time

        log_dict = {
            "method": request.method,
            "path": request.url.path,
            "params": str(request.query_params),
            "payload": payload,
            "status": response.status_code,
            "duration": duration,
        }

        logger.info(log_dict)
        return response
