from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class Transaction(BaseModel):
    id: UUID
    direction: Optional[str]
    txhash: Optional[str]
    currency: Optional[str]
    network: Optional[str]
    amount: Optional[float]
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
