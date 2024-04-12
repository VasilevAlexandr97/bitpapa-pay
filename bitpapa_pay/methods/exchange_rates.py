from typing import Dict, Literal, Type

from pydantic import BaseModel

from bitpapa_pay.methods.base import BaseMethod, BaseOutData


class GetExchangeRatesOut(BaseModel):
    rates: Dict[str, float]


class GetExchangeRates(BaseMethod):
    @property
    def endpoint(self) -> str:
        return "/api/v1/exchange_rates/all"

    @property
    def request_type(self) -> Literal["GET"]:
        return "GET"

    @property
    def returning_model(self) -> Type[GetExchangeRatesOut]:
        return GetExchangeRatesOut

    def get_data(self) -> BaseOutData:
        return BaseOutData(
            endpoint=self.endpoint,
            request_type=self.request_type,
            returning_model=self.returning_model
        )
