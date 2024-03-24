from typing import Type

from bitpapa_pay import types
from bitpapa_pay.methods.base import BaseMethod


class GetExchangeRatesAll(BaseMethod):
    _request_type: str = "GET"
    _endpoint: str = "/api/v1/exchange_rates/all"
    _returning: Type[types.ExchangeRatesAll] = types.ExchangeRatesAll
