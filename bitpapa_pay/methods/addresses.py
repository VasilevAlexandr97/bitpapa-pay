from typing import Literal, Optional, Type, Union

from bitpapa_pay.methods.base import BaseMethod, BaseOutData
from bitpapa_pay.schemas.addresses import (CreateAddressInputData,
                                           CreateAddressOutputData,
                                           GetAddressesOutputData,
                                           GetAddressesParams,
                                           GetAddressTransactionsOutputData,
                                           GetTransactionsOutputData,
                                           NewTransactionInputData,
                                           NewTransactionOutputData,
                                           RefillTransactionInputData,
                                           RefillTransactionOutputData,
                                           WithdrawalTransactionInputData,
                                           WithdrawalTransactionOutputData)


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
    def returning_model(self) -> Type[GetAddressTransactionsOutputData]:
        return GetAddressTransactionsOutputData

    def get_data(self) -> BaseOutData:
        return BaseOutData(
            endpoint=self.endpoint,
            request_type=self.request_type,
            returning_model=self.returning_model
        )


class NewTransaction(BaseMethod):
    def __init__(
        self,
        currency: str,
        amount: Union[int, float],
        from_address: str,
        to_address: str,
        network: str,
        label: str = ""
    ) -> None:
        self.direction = "offchain"
        self.currency = currency
        self.amount = amount
        self.from_address = from_address
        self.to_address = to_address
        self.netwok = network
        self.label = label

    @property
    def endpoint(self) -> str:
        return "/a3s/v1/transactions/new"

    @property
    def request_type(self) -> Literal["POST"]:
        return "POST"

    @property
    def returning_model(self) -> Type[NewTransactionOutputData]:
        return NewTransactionOutputData

    def get_data(self) -> BaseOutData:
        return BaseOutData(
            endpoint=self.endpoint,
            request_type=self.request_type,
            json_data=NewTransactionInputData(
                direction=self.direction,
                currency=self.currency,
                amount=self.amount,
                from_address=self.from_address,
                to_address=self.to_address,
                network=self.netwok,
                label=self.label
            ).model_dump(by_alias=True),
            returning_model=self.returning_model
        )


class RefillTransaction(BaseMethod):
    def __init__(
        self,
        currency: str,
        amount: Union[int, float],
        from_address: str,
        network: str,
        label: str = ""
    ) -> None:
        self.direction = "withdraw"
        self.currency = currency
        self.amount = amount
        self.from_address = from_address
        self.netwok = network
        self.label = label

    @property
    def endpoint(self) -> str:
        return "/a3s/v1/master/refill"

    @property
    def request_type(self) -> Literal["POST"]:
        return "POST"

    @property
    def returning_model(self) -> Type[RefillTransactionOutputData]:
        return RefillTransactionOutputData

    def get_data(self) -> BaseOutData:
        return BaseOutData(
            endpoint=self.endpoint,
            request_type=self.request_type,
            json_data=RefillTransactionInputData(
                direction=self.direction,
                currency=self.currency,
                amount=self.amount,
                from_address=self.from_address,
                network=self.netwok,
                label=self.label
            ).model_dump(by_alias=True),
            returning_model=self.returning_model
        )


class WithdrawalTransaction(BaseMethod):
    def __init__(
        self,
        currency: str,
        amount: Union[int, float],
        to_address: str,
        network: str,
        label: str = ""
    ) -> None:
        self.direction = "withdrawal"
        self.currency = currency
        self.amount = amount
        self.to_address = to_address
        self.netwok = network
        self.label = label

    @property
    def endpoint(self) -> str:
        return "/a3s/v1/master/withdrawal"

    @property
    def request_type(self) -> Literal["POST"]:
        return "POST"

    @property
    def returning_model(self) -> Type[WithdrawalTransactionOutputData]:
        return WithdrawalTransactionOutputData

    def get_data(self) -> BaseOutData:
        return BaseOutData(
            endpoint=self.endpoint,
            request_type=self.request_type,
            json_data=WithdrawalTransactionInputData(
                direction=self.direction,
                currency=self.currency,
                amount=self.amount,
                to_address=self.to_address,
                network=self.netwok,
                label=self.label
            ).model_dump(by_alias=True),
            returning_model=self.returning_model
        )
