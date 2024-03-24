from typing import Type, Union

from pydantic import BaseModel

from bitpapa_pay import types
from bitpapa_pay.methods.base import BaseMethod


class TelegramInvoice(BaseModel):
    currency_code: str
    amount: Union[int, float]


class CreateTelegramInvoice(BaseMethod):
    _request_type: str = "POST"
    _endpoint: str = "/api/v1/invoices/public"
    _returning: Type[types.TelegramInvoice] = types.TelegramInvoice

    api_token: str
    invoice: TelegramInvoice
