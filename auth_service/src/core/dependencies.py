# stdlib
from typing import Annotated

# third party
from src.core.database import get_async_db
from sqlalchemy.ext.asyncio import AsyncSession

# fastapi
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

DBSessionDep = Annotated[AsyncSession, Depends(get_async_db)]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")
