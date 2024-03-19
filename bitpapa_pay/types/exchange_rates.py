from pydantic import BaseModel


class ExchangeRatesAll(BaseModel):
    rates: dict
