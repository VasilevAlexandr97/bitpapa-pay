from bitpapa_pay import types
from bitpapa_pay.methods.base import BaseMethod


class GetTelegramInvoices(BaseMethod):
    _request_type: str = "GET"
    _endpoint: str = "/api/v1/invoices/public"
    _returning: type[types.TelegramInvoices] = types.TelegramInvoices

    api_token: str
