from typing import Type

from bitpapa_pay import types
from bitpapa_pay.methods.base import BaseMethod


class GetTelegramInvoices(BaseMethod):
    _request_type: str = "GET"
    _endpoint: str = "/api/v1/invoices/public"
    _returning: Type[types.TelegramInvoices] = types.TelegramInvoices

    api_token: str
