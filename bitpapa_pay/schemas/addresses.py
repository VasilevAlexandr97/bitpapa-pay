from typing import List, Optional, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


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


class WithdrawalTransactionInputData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    direction: str = Field(default="withdrawal")
    currency: str
    amount: Union[int, float]
    to_address: str = Field(alias="to")
    network: str
    label: str = ""


class WithdrawalTransactionOutputData(BaseModel):
    transaction: Transaction


class RefillTransactionInputData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    direction: str = Field(default="refill")
    currency: str
    amount: Union[int, float]
    from_address: str = Field(alias="from")
    network: str
    label: str = Field(default="")


class RefillTransactionOutputData(BaseModel):
    transaction: Transaction
