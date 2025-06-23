# stdlib
from typing import Any
from urllib.parse import parse_qs

# third party
import httpx

# fastapi
from fastapi import Request, Response
from fastapi.responses import JSONResponse


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

    def _get_params(self, path: str, request: Request) -> tuple[str, dict[str, Any]]:
        """
        Extracts and combines query parameters from the path and the request.

        Args:
            path: The request path, which may contain query parameters.
            request: The incoming request object.

        Returns:
            A tuple containing the actual path without query parameters,
            and a dictionary of all combined query parameters.
        """
        actual_path = path
        additional_params = {}
        if "?" in actual_path:
            parts = actual_path.split("?", 1)
            actual_path = parts[0]
            if len(parts) > 1:
                query_string = parts[1]
                parsed_params = parse_qs(query_string)
                additional_params = {
                    k: v[0] if len(v) == 1 else v for k, v in parsed_params.items()
                }

        all_params: dict[str, Any] = dict(request.query_params.multi_items())
        all_params.update(additional_params)

        return actual_path, all_params

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

        actual_path, all_params = self._get_params(path, request)

        # For GET/DELETE requests, body is an empty dict and we shouldn't send it.
        # For other methods, body is parsed by FastAPI and we should send it as json.
        json_body = body if request.method in ["POST", "PUT", "PATCH"] else None

        async with httpx.AsyncClient() as client:
            url = f"http://{service}-service:8000/{actual_path}"
            response = await client.request(
                method=request.method,
                url=url,
                headers=headers,
                params=all_params,
                json=json_body,
                timeout=30.0,
            )
            return Response(
                content=response.content,
                status_code=response.status_code,
                media_type=response.headers.get("content-type", "text/plain"),
            )

    async def call_openapi(self, service: str) -> JSONResponse:
        """
        Fetches and rewrites the OpenAPI JSON from the microservice.
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"http://{service}-service:8000/openapi.json"
                )
                openapi_json = response.json()
                openapi_json["servers"] = [{"url": f"/{service}"}]

                return JSONResponse(content=openapi_json)
            except httpx.RequestError as e:
                return JSONResponse(
                    status_code=502,
                    content={
                        "error": f"Failed to fetch OpenAPI for {service}: {str(e)}"
                    },
                )


def get_gateway_service():
    return GatewayService()
