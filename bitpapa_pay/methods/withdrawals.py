from typing import Literal, Type

from bitpapa_pay.methods.base import BaseMethod, BaseOutData
from bitpapa_pay.schemas.withdrawals import GetWithdrawalFeesOutputData


class GetWithdrawalFees(BaseMethod):
    @property
    def endpoint(self) -> str:
        return "/api/v1/withdrawals/withdrawal_fees"

    @property
    def request_type(self) -> Literal["GET"]:
        return "GET"

    @property
    def returning_model(self) -> Type[GetWithdrawalFeesOutputData]:
        return GetWithdrawalFeesOutputData

    def get_data(self) -> BaseOutData:
        return BaseOutData(
            endpoint=self.endpoint,
            request_type=self.request_type,
            returning_model=self.returning_model
        )
