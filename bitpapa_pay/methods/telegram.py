from typing import Literal, Type, Union, Optional

from bitpapa_pay.methods.base import BaseMethod, BaseOutData
from bitpapa_pay.types.telegram import (CreateTelegramInvoiceInputData,
                                        CreateTelegramInvoiceOutputData,
                                        GetTelegramInvoicesInputParams,
                                        TelegramInvoiceInputData,
                                        TelegramInvoices)


class CreateTelegramInvoice(BaseMethod):
    def __init__(
        self,
        api_token: str,
        currency_code: str,
        amount: Union[int, float],
        crypto_address: Optional[str] = None
    ) -> None:
        self.api_token = api_token
        self.currency_code = currency_code
        self.amount = amount
        self.crypto_address = crypto_address

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
                    amount=self.amount,
                    crypto_address=self.crypto_address
                ),
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
