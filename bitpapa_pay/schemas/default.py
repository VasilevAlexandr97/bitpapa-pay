from typing import Dict, List, Optional, Union

from pydantic import BaseModel


class GetExchangeRatesResponse(BaseModel):
    rates: Dict[str, float]


class FeeData(BaseModel):
    amount_min: Union[int, float]
    amount_max: Optional[Union[int, float]]
    fee: Union[int, float]
    network: str


class GetWithdrawalFeesResponse(BaseModel):
    withdrawal_fees: Dict[str, List[FeeData]]
