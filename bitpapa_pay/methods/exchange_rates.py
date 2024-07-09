from typing import Literal, Type

from bitpapa_pay.methods.base import BaseMethod, BaseOutData
from bitpapa_pay.schemas.exchange_rates import GetExchangeRatesOutputData


class GetExchangeRates(BaseMethod):
    @property
    def endpoint(self) -> str:
        return "/api/v1/exchange_rates/all"

    @property
    def request_type(self) -> Literal["GET"]:
        return "GET"

    @property
    def returning_model(self) -> Type[GetExchangeRatesOutputData]:
        return GetExchangeRatesOutputData

    def get_data(self) -> BaseOutData:
        return BaseOutData(
            endpoint=self.endpoint,
            request_type=self.request_type,
            returning_model=self.returning_model
        )
