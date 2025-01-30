from typing import List, Optional, Union
from uuid import UUID

from pydantic import BaseModel


class Address(BaseModel):
    id: UUID
    address: Optional[str]
    currency: Optional[str]
    network: Optional[str]
    balance: Optional[Union[int, float]]
    label: str


class GetAddressesResponse(BaseModel):
    addresses: List[Address]


class CreateAddressResponse(BaseModel):
    address: Address

