from typing import Optional

from bitpapa_pay.enums import RequestType
from bitpapa_pay.methods.base import BaseMethod


class GetAddressesMethod(BaseMethod):
    endpoint: str = "/a3s/v1/addresses"
    request_type: RequestType = RequestType.GET
    currency: Optional[str] = None
    label: Optional[str] = None


class CreateAddressMethod(BaseMethod):
    endpoint: str = "/a3s/v1/addresses/new"
    request_type: RequestType = RequestType.POST
    currency: str
    network: str
    label: str = ""
