from typing import List, Literal, Type, Union

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


class TelegramInvoiceInputData(BaseModel):
    currency_code: str
    amount: Union[int, float]


class CreateTelegramInvoiceInputData(BaseModel):
    api_token: str
    invoice: TelegramInvoiceInputData


class CreateTelegramInvoiceOutputData(BaseModel):
    invoice: TelegramInvoice


class GetTelegramInvoicesInputParams(BaseModel):
    api_token: str


class CreateTelegramInvoice(BaseMethod):
    def __init__(
        self,
        api_token: str,
        currency_code: str,
        amount: Union[int, float]
    ) -> None:
        self.api_token = api_token
        self.currency_code = currency_code
        self.amount = amount

    @property
    def endpoint(self) -> str:
        return "/api/v1/invoices/public"

    @property
    def request_type(self) -> Literal["POST"]:
        return "POST"

    @property
    def returning_model(self) -> Type[CreateTelegramInvoiceOutputData]:
        return CreateTelegramInvoiceOutputData

    def get_data(self) -> BaseOutData:
        return BaseOutData(
            endpoint=self.endpoint,
            request_type=self.request_type,
            json_data=CreateTelegramInvoiceInputData(
                api_token=self.api_token,
                invoice=TelegramInvoiceInputData(
                    currency_code=self.currency_code,
                    amount=self.amount
                )
            ).model_dump(),
            returning_model=self.returning_model
        )


class GetTelegramInvoices(BaseMethod):
    def __init__(self, api_token: str) -> None:
        self.api_token = api_token

    @property
    def endpoint(self) -> str:
        return "/api/v1/invoices/public"

    @property
    def request_type(self) -> Literal["GET"]:
        return "GET"

    @property
    def returning_model(self) -> Type[TelegramInvoices]:
        return TelegramInvoices

    def get_data(self) -> BaseOutData:
        return BaseOutData(
            endpoint=self.endpoint,
            request_type=self.request_type,
            params=GetTelegramInvoicesInputParams(
                api_token=self.api_token
            ).model_dump(),
            returning_model=self.returning_model
        )
