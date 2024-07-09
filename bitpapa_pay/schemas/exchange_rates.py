from typing import Dict

from pydantic import BaseModel


class GetExchangeRatesOutputData(BaseModel):
    rates: Dict[str, float]
