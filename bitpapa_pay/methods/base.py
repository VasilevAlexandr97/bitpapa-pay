from abc import ABC, abstractmethod
from typing import Any, Literal

from bitpapa_pay.types.base import BaseOutData


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
