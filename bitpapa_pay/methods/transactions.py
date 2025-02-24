from pydantic import Field

from bitpapa_pay.enums import RequestType
from bitpapa_pay.methods.base import BaseMethod


class GetTransactionsMethod(BaseMethod):
    endpoint: str = "/a3s/v1/transactions"
    request_type: RequestType = RequestType.GET
    page: int = 1
    limit: int = 100


class GetAddressTransactionMethod(BaseMethod):
    endpoint: str = ""
    request_type: RequestType = RequestType.GET
    uuid: str
    page: int = 1
    limit: int = 100

    def model_post_init(self, __context):
        self.endpoint = f"/a3s/v1/address/{self.uuid}/transactions"


class CreateTransactionMethod(BaseMethod):
    endpoint: str = "/a3s/v1/transactions/new"
    request_type: RequestType = RequestType.POST
    currency: str
    amount: float
    direction: str = "offchain"
    from_address: str = Field(..., alias="from")
    to_address: str = Field(..., alias="to")
    network: str
    label: str = ""


class MasterWithdrawalTransactionMethod(BaseMethod):
    endpoint: str = "/a3s/v1/master/withdrawal"
    request_type: RequestType = RequestType.POST
    currency: str
    amount: float
    to_address: str = Field(..., alias="to")
    network: str
    label: str = ""


class MasterRefillTransactionMethod(BaseMethod):
    endpoint: str = "/a3s/v1/master/refill"
    request_type: RequestType = RequestType.POST
    direction: str = "withdraw"
    currency: str
    amount: float
    from_address: str = Field(..., alias="from")
    network: str
    label: str = ""
