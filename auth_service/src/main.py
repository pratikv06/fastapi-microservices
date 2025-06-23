# stdlib
from typing import Any

# fastapi
from fastapi import Body, Query, FastAPI

app = FastAPI(title="Auth Service")


@app.get("/health")
async def health(
    q: str = Query(default=""),
) -> dict[str, Any]:
    return {
        "status": "ok",
        "service": "auth",
        "query_params": q,
    }


@app.post("/health2")
async def health2(
    q: str = Query(default=""),
    body: dict[str, Any] = Body(..., description="The body of the request"),
) -> dict[str, Any]:
    return {
        "status": "ok2",
        "service": "auth2",
        "query_params": q,
        "body": body,
    }


@app.put("/health3")
async def health3(
    body: dict[str, Any] = Body(..., description="The body of the request"),
) -> dict[str, Any]:
    return {
        "status": "ok",
        "service": "auth",
        "body": body,
    }


@app.patch("/health4")
async def health4(
    body: dict[str, Any] = Body(..., description="The body of the request"),
) -> dict[str, Any]:
    return {
        "status": "ok",
        "service": "auth",
        "body": body,
    }


@app.delete("/health5")
async def health5(
    q: str = Query(default=""),
) -> dict[str, Any]:
    return {
        "status": "ok",
        "service": "auth",
        "query_params": q,
    }
