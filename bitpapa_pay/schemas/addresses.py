from typing import List, Optional, Union
from uuid import UUID

from pydantic import BaseModel, Field


class Address(BaseModel):
    id: UUID
    address: Optional[str]
    currency: str
    network: str
    balance: Optional[Union[int, float]]
    label: str


class GetAddressesOutputData(BaseModel):
    addresses: List[Address]


class GetAddressesParams(BaseModel):
    currency: Optional[str] = None
    label: Optional[str] = None


class CreateAddressInputData(BaseModel):
    currency: str
    network: str
    label: str


class CreateAddressOutputData(BaseModel):
    address: Address


class Transaction(BaseModel):
    id: UUID
    direction: str
    txhash: Optional[str]
    currency: str
    network: Optional[str]
    amount: Union[str, float]
    from_: Optional[str] = Field(alias="from")
    to: Optional[str]
    input: Optional[str]
    label: Optional[str]


class GetTransactionsOutputData(BaseModel):
    transaction: List[Transaction]
