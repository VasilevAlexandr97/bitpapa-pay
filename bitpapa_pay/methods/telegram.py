from typing import List, Type, Union

from pydantic import BaseModel, computed_field

from bitpapa_pay.methods.base import BaseMethod, BaseOutData


class TelegramInvoice(BaseModel):
    id: str
    currency_code: str
    amount: Union[int, float]
    status: str
    created_at: str
    updated_at: str

    @computed_field
    def url(self) -> str:
        return f"https://t.me/bitpapa_bot?start={self.id}"


class TelegramInvoices(BaseModel):
    invoices: List[TelegramInvoice]


class TelegramInvoiceIn(BaseModel):
    currency_code: str
    amount: Union[int, float]


class CreateTelegramInvoiceJD(BaseModel):
    api_token: str
    invoice: TelegramInvoiceIn


class CreateTelegramInvoiceOut(BaseModel):
    invoice: TelegramInvoice


class GetTelegramInvoicesParams(BaseModel):
    api_token: str


class CreateTelegramInvoice(BaseMethod):
    def __init__(
        self,
        api_token: str,
        currency_code: str,
        amount: Union[int, float]
    ) -> None:
        self.returning_model: Type[CreateTelegramInvoiceOut] = CreateTelegramInvoiceOut
        self.api_token = api_token
        self.currency_code = currency_code
        self.amount = amount

    @property
    def endpoint(self) -> str:
        return "/api/v1/invoices/public"

    def get_data(self) -> BaseOutData:
        return BaseOutData(
            endpoint=self.endpoint,
            request_type="POST",
            json_data=CreateTelegramInvoiceJD(
                api_token=self.api_token,
                invoice=TelegramInvoiceIn(
                    currency_code=self.currency_code,
                    amount=self.amount
                )
            ).model_dump(),
            returning_model=self.returning_model
        )


class GetTelegramInvoices(BaseMethod):
    def __init__(self, api_token: str) -> None:
        self.returning_model: Type[TelegramInvoices] = TelegramInvoices
        self.api_token = api_token

    @property
    def endpoint(self) -> str:
        return "/api/v1/invoices/public"

    def get_data(self) -> BaseOutData:
        return BaseOutData(
            endpoint=self.endpoint,
            request_type="GET",
            params=GetTelegramInvoicesParams(
                api_token=self.api_token
            ).model_dump(),
            returning_model=self.returning_model
        )
