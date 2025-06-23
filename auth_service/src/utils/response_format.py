# stdlib
from typing import Any, Dict

# third party
from pydantic import BaseModel


class APIResponse(BaseModel):
    status: int
    message: str = ""
    data: Dict[str, Any] | list[Dict[str, Any]] | Any = {}
    error: str = ""

    def __repr__(self):
        return f'APIResponse(status={self.status}, message="{self.message}", data={self.data}, error="{self.error})"'

    def __str__(self):
        return self.__repr__()
