from typing import List, Optional, Union

from pydantic import BaseModel, computed_field


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
    crypto_address: Optional[str]


class CreateTelegramInvoiceInputData(BaseModel):
    api_token: str
    invoice: TelegramInvoiceInputData


class CreateTelegramInvoiceOutputData(BaseModel):
    invoice: TelegramInvoice


class GetTelegramInvoicesInputParams(BaseModel):
    api_token: str
