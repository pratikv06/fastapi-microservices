# stdlib
from typing import Any, Annotated

# third party
from src.services.gateway import GatewayService, get_gateway_service

# fastapi
from fastapi import Body, Depends, Request, Response, APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="",
    tags=["Proxy Gateway"],
)

GatewayServiceDep = Annotated[GatewayService, Depends(get_gateway_service)]


# === Proxy and rewrite OpenAPI JSON ===
@router.get("/{service}/openapi.json", include_in_schema=False)
async def get_service_openapi(
    service: str,
    gateway_service: GatewayServiceDep,
) -> JSONResponse:
    """
    Fetches and rewrites the OpenAPI JSON from the microservice.

    Adds `servers` to include service path.
    """
    return await gateway_service.call_openapi(service)


@router.get(
    "/{service}/{path:path}",
    status_code=status.HTTP_200_OK,
    response_model=None,
)
async def gateway_proxy_service_get(
    service: str,
    path: str,
    request: Request,
    gateway_service: GatewayServiceDep,
) -> Response:
    return await gateway_service.call(service, path, request, body={})


@router.post(
    "/{service}/{path:path}",
    status_code=status.HTTP_201_CREATED,
    response_model=None,
)
async def gateway_proxy_service_post(
    service: str,
    path: str,
    request: Request,
    gateway_service: GatewayServiceDep,
    body: dict[str, Any] = Body(..., description="The body of the request"),
) -> Response:
    return await gateway_service.call(service, path, request, body)


@router.put(
    "/{service}/{path:path}",
    status_code=status.HTTP_200_OK,
    response_model=None,
)
async def gateway_proxy_service_put(
    service: str,
    path: str,
    request: Request,
    gateway_service: GatewayServiceDep,
    body: dict[str, Any] = Body(..., description="The body of the request"),
) -> Response:
    return await gateway_service.call(service, path, request, body)


@router.patch(
    "/{service}/{path:path}",
    status_code=status.HTTP_200_OK,
    response_model=None,
)
async def gateway_proxy_service_patch(
    service: str,
    path: str,
    request: Request,
    gateway_service: GatewayServiceDep,
    body: dict[str, Any] = Body(..., description="The body of the request"),
) -> Response:
    return await gateway_service.call(service, path, request, body)


@router.delete(
    "/{service}/{path:path}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
async def gateway_proxy_service_delete(
    service: str,
    path: str,
    request: Request,
    gateway_service: GatewayServiceDep,
) -> Response:
    return await gateway_service.call(service, path, request, body={})
