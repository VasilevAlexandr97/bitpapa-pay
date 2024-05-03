from typing import List, Optional, Union
from uuid import UUID

from pydantic import BaseModel


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


class GetTransactionsOutputData(BaseModel):
    transactions: List
