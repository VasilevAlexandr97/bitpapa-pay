from typing import List, Optional

from pydantic import BaseModel, computed_field


class Invoice(BaseModel):
    id: str
    invoice_type: str
    currency_code: str
    fiat_currency_code: Optional[str]
    merchant_invoice_id: Optional[str]
    amount: float
    fiat_amount: float
    status: str
    crypto_address: Optional[str]
    accepted_crypto: list
    paid_button_name: Optional[str]
    paid_button_url: Optional[str]
    created_at: str
    updated_at: str

    @computed_field
    def url(self) -> str:
        return f"https://t.me/bitpapa_bot?start={self.id}"


class CreateInvoiceResponse(BaseModel):
    invoice: Invoice


class GetInvoicesResponse(BaseModel):
    invoices: List[Invoice]
    page: int
    count: int
    pages: int
