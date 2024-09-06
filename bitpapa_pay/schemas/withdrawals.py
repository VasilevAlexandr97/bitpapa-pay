from pydantic import BaseModel
from typing import Union, Dict, List, Optional


class FeeData(BaseModel):
    amount_min: Union[int, float]
    amount_max: Optional[Union[int, float]]
    fee: Union[int, float]
    network: str


class GetWithdrawalFeesOutputData(BaseModel):
    withdrawal_fees: Dict[str, List[FeeData]]
