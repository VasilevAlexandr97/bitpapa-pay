from bitpapa_pay.enums import RequestType
from bitpapa_pay.methods.base import BaseMethod


class GetExchangeRateMetod(BaseMethod):
    endpoint: str = "/api/v1/exchange_rates/all"
    request_type: RequestType = RequestType.GET


class GetWithdrawalFeesMethod(BaseMethod):
    endpoint: str = "/api/v1/withdrawals/withdrawal_fees"
    request_type: RequestType = RequestType.GET
