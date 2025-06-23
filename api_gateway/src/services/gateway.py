# stdlib
from typing import Any

# third party
import httpx

# fastapi
from fastapi import Request, Response


class GatewayService:

    async def call(
        self,
        service: str,
        path: str,
        request: Request,
        body: dict[str, Any],
    ) -> Response:
        """
        Handles requests to API endpoints by proxying to the target service.
        """
        if path in ["docs", "redoc"]:
            return await self._call_docs(service, path)
        return await self._call_service(service, path, request, body)

    async def _call_docs(self, service: str, path: str) -> Response:
        """
        Handles requests to documentation endpoints (Swagger/ReDoc)
        by proxying to the target service.

        Args:
            service: Name of the service to get documentation from
            path: Documentation endpoint path ('docs' or 'redoc')

        Returns:
            Response containing the HTML documentation with updated OpenAPI URL
        """
        async with httpx.AsyncClient() as client:
            openapi_url: str = f"/{service}/openapi.json"
            url: str = f"http://{service}-service:8000/{path}?url={openapi_url}"
            response = await client.get(url)
            html = response.text.replace("/openapi.json", openapi_url)
            return Response(
                content=html,
                status_code=response.status_code,
                media_type="text/html",
            )

    async def _call_service(
        self,
        service: str,
        path: str,
        request: Request,
        body: dict[str, Any],
    ) -> Response:
        """
        Handles requests to API endpoints by proxying to the target service.

        Args:
            service: Name of the service to proxy the request to
            path: API endpoint path
            request: Incoming request object
            body: Body of the request

        Returns:
            Response containing the proxied service's response content,
            status code, and media type
        """

        # The 'body' argument is already parsed by FastAPI for POST/PUT/PATCH,
        # so we don't need to read the request stream again.
        # We also filter out headers that httpx should set itself.
        headers = {
            name: value
            for name, value in request.headers.items()
            if name.lower() not in ("host", "content-length", "content-type")
        }

        # For GET/DELETE requests, body is an empty dict and we shouldn't send it.
        # For other methods, body is parsed by FastAPI and we should send it as json.
        json_body = body if request.method in ["POST", "PUT", "PATCH"] else None

        async with httpx.AsyncClient() as client:
            url = f"http://{service}-service:8000/{path}"
            response = await client.request(
                method=request.method,
                url=url,
                headers=headers,
                params=dict(request.query_params),
                json=json_body,
                timeout=30.0,
            )
            return Response(
                content=response.content,
                status_code=response.status_code,
                media_type=response.headers.get("content-type", "text/plain"),
            )


def get_gateway_service():
    return GatewayService()
