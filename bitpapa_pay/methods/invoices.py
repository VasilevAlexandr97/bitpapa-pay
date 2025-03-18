from typing import List, Optional, Dict, Any

from pydantic import model_validator

from bitpapa_pay.enums import (
    CryptoCurrencyCode,
    InvoiceType,
    PaidButtonType,
    RequestType,
)
from bitpapa_pay.methods import BaseMethod


class CreateInvoiceMethod(BaseMethod):
    endpoint: str = "/api/v1/invoices/public"
    request_type: RequestType = RequestType.POST
    invoice_type: str
    expiration_time: Optional[int] = None
    merchant_invoice_id: Optional[str] = None
    paid_button_name: Optional[str] = None
    paid_button_url: Optional[str] = None
    private_message: Optional[str] = None
    crypto_address: Optional[str] = None

    __max_length_private_message = 1000

    @model_validator(mode="after")
    def _validate_paid_buttons(self) -> "CreateInvoiceMethod":
        paid_button_name_filled = (
            self.paid_button_name is not None
            and self.paid_button_name.strip() != ""
        )
        paid_button_url_filled = (
            self.paid_button_url is not None
            and self.paid_button_url.strip() != ""
        )
        if (paid_button_name_filled and not paid_button_url_filled) or (
            not paid_button_name_filled and paid_button_url_filled
        ):
            raise ValueError(
                "Both 'paid_button_name' and 'paid_button_url' must "
                "be provided together or both must be None.",
            )
        return self

    @model_validator(mode="after")
    def _validate_paid_button_name(self) -> "CreateInvoiceMethod":
        if self.paid_button_name is not None and self.paid_button_name not in [
            i.value for i in PaidButtonType
        ]:
            raise ValueError(
                "paid_button_name must be one of "
                f"{[i.value for i in PaidButtonType]}"
            )
        return self

    @model_validator(mode="after")
    def _validate_paid_button_url(self) -> "CreateInvoiceMethod":
        if self.paid_button_url is not None and not self.paid_button_url:
            raise ValueError(
                "paid_button_url must be a valid URL.",
            )
        return self

    @model_validator(mode="after")
    def _validate_private_message(self) -> "CreateInvoiceMethod":
        if (
            self.private_message is not None
            and len(self.private_message) >= self.__max_length_private_message
        ):
            raise ValueError(
                "Private message must be less or equal 1000 characters.",
            )
        return self


class CreateCryptoInvoiceMethod(CreateInvoiceMethod):
    amount: float
    currency_code: str
    invoice_type: str = InvoiceType.CRYPTO.value

    @model_validator(mode="after")
    def _validate_currency_code(self) -> "CreateCryptoInvoiceMethod":
        if self.currency_code not in [i.value for i in CryptoCurrencyCode]:
            raise ValueError(
                "currency_code must be one of "
                f"{[i.value for i in CryptoCurrencyCode]}"
            )
        return self

    def to_payload(self) -> Dict[str, Any]:
        return {
            "invoice": self.model_dump(
                exclude={"endpoint", "request_type", "api_token"},
                by_alias=True,
            ),
        }


class CreateFiatInvoiceMethod(CreateInvoiceMethod):
    accepted_crypto: List[str]
    fiat_amount: float
    fiat_currency_code: str
    invoice_type: str = InvoiceType.FIAT.value

    def to_payload(self) -> Dict[str, Any]:
        return {
            "invoice": self.model_dump(
                exclude={"endpoint", "request_type", "api_token"},
                by_alias=True,
            ),
        }


class GetInvoicesMethod(BaseMethod):
    endpoint: str = "/api/v1/invoices/public"
    request_type: RequestType = RequestType.GET
    page: int = 1
