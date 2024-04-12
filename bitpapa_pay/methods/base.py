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

    @property
    @abstractmethod
    def request_type(self) -> Literal["GET", "POST"]:
        pass

    @property
    @abstractmethod
    def returning_model(self) -> Any:
        pass

    def set_params(self, params: dict) -> dict:
        return {key: params[key] for key in params if params[key] is not None}

    @abstractmethod
    def get_data(self) -> BaseOutData:
        pass
