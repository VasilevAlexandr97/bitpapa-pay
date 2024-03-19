from typing import Any

from pydantic import BaseModel


class BaseMethod(BaseModel):
    _request_type: str
    _endpoint: str
    _returning: Any
