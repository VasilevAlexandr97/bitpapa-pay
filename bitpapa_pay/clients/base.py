from abc import ABC, abstractmethod
from typing import Final

from aiohttp import ClientResponse

from bitpapa_pay.exceptions import (RESPONSE_STATUS_401, RESPONSE_STATUS_404,
                                    RESPONSE_STATUS_500)

DEFAULT_TIMEOUT: Final[float] = 60.0


class Client(ABC):
    def __init__(self, timeout: float | None = DEFAULT_TIMEOUT) -> None:
        self.timeout = timeout

    @abstractmethod
    def _create_session(self):
        pass

    async def check_response(self, response: ClientResponse):
        if response.status == 200:
            return await response.json()
        elif response.status == 401:
            raise RESPONSE_STATUS_401
        elif response.status == 404:
            raise RESPONSE_STATUS_404("Endpoint not found")
        elif response.status == 500:
            raise RESPONSE_STATUS_500
