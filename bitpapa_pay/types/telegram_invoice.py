from pydantic import BaseModel, computed_field


class Invoice(BaseModel):
    id: str
    currency_code: str
    amount: int | float
    status: str
    created_at: str
    updated_at: str

    @computed_field
    def url(self) -> str:
        return f"https://t.me/bitpapa_bot?start={self.id}"


class TelegramInvoice(BaseModel):
    invoice: Invoice


class TelegramInvoices(BaseModel):
    invoices: list[Invoice]
