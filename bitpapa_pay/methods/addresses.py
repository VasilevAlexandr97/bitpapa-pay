from typing import Literal, Optional, Type

from bitpapa_pay.methods.base import BaseMethod, BaseOutData
from bitpapa_pay.schemas.addresses import (CreateAddressInputData,
                                           CreateAddressOutputData,
                                           GetAddressesOutputData,
                                           GetAddressesParams,
                                           GetTransactionsOutputData)


class GetAddresses(BaseMethod):
    def __init__(
        self,
        currency: Optional[str] = None,
        label: Optional[str] = None
    ) -> None:
        self.currency = currency
        self.label = label

    @property
    def endpoint(self) -> str:
        return "/a3s/v1/addresses"

    @property
    def request_type(self) -> Literal["GET"]:
        return "GET"

    @property
    def returning_model(self) -> Type[GetAddressesOutputData]:
        return GetAddressesOutputData

    def get_data(self) -> BaseOutData:
        return BaseOutData(
            endpoint=self.endpoint,
            request_type=self.request_type,
            params=self.set_params(GetAddressesParams(
                currency=self.currency,
                label=self.label
            ).model_dump()),
            returning_model=self.returning_model
        )


class CreateAddress(BaseMethod):
    def __init__(
        self,
        currency: str,
        network: str,
        label: str = "",
    ) -> None:
        self.currency = currency
        self.label = label
        self.network = network

    @property
    def endpoint(self) -> str:
        return "/a3s/v1/addresses/new"

    @property
    def request_type(self) -> Literal["POST"]:
        return "POST"

    @property
    def returning_model(self) -> Type[CreateAddressOutputData]:
        return CreateAddressOutputData

    def get_data(self) -> BaseOutData:
        return BaseOutData(
            endpoint=self.endpoint,
            request_type=self.request_type,
            json_data=CreateAddressInputData(
                currency=self.currency,
                network=self.network,
                label=self.label
            ).model_dump(),
            returning_model=self.returning_model
        )


class GetTransactions(BaseMethod):
    @property
    def endpoint(self) -> str:
        return "/a3s/v1/transactions"

    @property
    def request_type(self) -> Literal["GET"]:
        return "GET"

    @property
    def returning_model(self) -> Type[GetTransactionsOutputData]:
        return GetTransactionsOutputData

    def get_data(self) -> BaseOutData:
        return BaseOutData(
            endpoint=self.endpoint,
            request_type=self.request_type,
            returning_model=self.returning_model
        )


class GetAddressTransactions(BaseMethod):
    def __init__(self, uuid: str) -> None:
        self.uuid = uuid

    @property
    def endpoint(self) -> str:
        return f"/a3s/v1/address/{self.uuid}/transactions"

    @property
    def request_type(self) -> Literal["GET"]:
        return "GET"

    @property
    def returning_model(self) -> Type[GetTransactionsOutputData]:
        return GetTransactionsOutputData

    def get_data(self) -> BaseOutData:
        return BaseOutData(
            endpoint=self.endpoint,
            request_type=self.request_type,
            returning_model=self.returning_model
        )
