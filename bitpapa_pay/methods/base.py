from abc import ABC, abstractmethod
from typing import Any, Literal, Optional

from pydantic import BaseModel


class BaseOutData(BaseModel):
    endpoint: str
    request_type: Literal["GET", "POST"]
    params: Optional[dict] = None
    json_data: Optional[dict] = None
    returning_model: Any


class BaseMethod(ABC):
    @property
    @abstractmethod
    def endpoint(self) -> str:
        pass

    @abstractmethod
    def get_data(self) -> BaseOutData:
        pass
