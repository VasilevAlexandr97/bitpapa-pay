from typing import Dict, Type

from pydantic import BaseModel

from bitpapa_pay.methods.base import BaseMethod, BaseOutData


class GetExchangeRatesOut(BaseModel):
    rates: Dict[str, float]


class GetExchangeRates(BaseMethod):
    def __init__(self) -> None:
        self.returning_model: Type[GetExchangeRatesOut] = GetExchangeRatesOut

    @property
    def endpoint(self) -> str:
        return "/api/v1/exchange_rates/all"

    def get_data(self) -> BaseOutData:
        return BaseOutData(
            endpoint=self.endpoint,
            request_type="GET",
            returning_model=self.returning_model
        )
