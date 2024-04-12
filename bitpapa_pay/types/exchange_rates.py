from typing import Dict

from pydantic import BaseModel


class GetExchangeRatesOut(BaseModel):
    rates: Dict[str, float]
