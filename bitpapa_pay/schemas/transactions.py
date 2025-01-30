from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class Transaction(BaseModel):
    id: UUID
    direction: str
    txhash: Optional[str]
    currency: str
    network: Optional[str]
    amount: float
    from_address: Optional[str] = Field(alias="from")
    to_address: Optional[str] = Field(alias="to")
    input: Optional[str]
    label: Optional[str]


class TransactionResponse(BaseModel):
    transaction: Transaction


class GetAddressTransactionsResponse(BaseModel):
    transaction: List[Transaction]


class GetTransactionsResponse(BaseModel):
    transactions: List[Transaction]
