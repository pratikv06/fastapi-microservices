# third party
from src.api.routes import routers

# local
from src.core.settings import settings

# fastapi
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    **settings.APP_DETAILS,
    debug=settings.DEBUG,
)

# Add Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Routers
for router in routers:
    app.include_router(router)


@app.get("/health-check")
async def health_check():
    return {
        "status": "ok",
        "message": "API Gateway is running",
    }
