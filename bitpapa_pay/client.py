from typing import List, Optional

from aiohttp import ClientError, ClientSession
from loguru import logger

from bitpapa_pay.enums import RequestType
from bitpapa_pay.exceptions import BadRequestError
from bitpapa_pay.methods import (
    BaseMethod,
    CreateAddressMethod,
    CreateCryptoInvoiceMethod,
    CreateFiatInvoiceMethod,
    CreateTransactionMethod,
    GetAddressesMethod,
    GetAddressTransactionMethod,
    GetExchangeRateMetod,
    GetInvoicesMethod,
    GetTransactionsMethod,
    GetWithdrawalFeesMethod,
    MasterRefillTransactionMethod,
    MasterWithdrawalTransactionMethod,
)
from bitpapa_pay.schemas import (
    CreateAddressResponse,
    CreateInvoiceResponse,
    GetAddressesResponse,
    GetAddressTransactionsResponse,
    GetExchangeRatesResponse,
    GetInvoicesResponse,
    GetTransactionsResponse,
    GetWithdrawalFeesResponse,
    TransactionResponse,
)


class HttpClient:
    BASE_URL = "https://bitpapa.com"

    def __init__(self, api_token: str, debug: bool = False) -> None:
        self._debug = debug
        self._api_token = api_token
        self._session: Optional[ClientSession] = None

    def debug_message(self, message: str):
        if self._debug:
            logger.debug(message)

    def get_headers(self):
        return {
            "Content-Type": "application/json",
            "User-Agent": "python/pkg/bitpapa-pay",
            "X-Access-Token": self._api_token,
        }

    def get_session(self) -> ClientSession:
        headers = self.get_headers()
        self.debug_message(f"request headers: {headers}")

        if isinstance(self._session, ClientSession):
            return self._session
        self._session = ClientSession(base_url=self.BASE_URL, headers=headers)
        return self._session

    async def close(self):
        if isinstance(self._session, ClientSession):
            await self._session.close()

    async def _get_request(
        self,
        session: ClientSession,
        endpoint: str,
        params: Optional[dict] = None,
    ):
        async with session.get(url=endpoint, params=params) as resp:
            self.debug_message(f"status: {resp.status}")
            resp.raise_for_status()
            return await resp.json()

    async def _post_request(
        self,
        session: ClientSession,
        endpoint: str,
        json_data: Optional[dict] = None,
    ):
        async with session.post(url=endpoint, json=json_data) as resp:
            self.debug_message(f"status: {resp.status}")
            resp.raise_for_status()
            return await resp.json()

    async def _make_request(self, method: BaseMethod):
        session = self.get_session()
        self.debug_message(
            f"request url: {self.BASE_URL}{method.endpoint}",
        )
        try:
            if method.request_type == RequestType.GET:
                params = method.to_params()
                self.debug_message(f"params: {params}")
                result = await self._get_request(
                    session=session,
                    endpoint=method.endpoint,
                    params=params,
                )
            elif method.request_type == RequestType.POST:
                payload_data = method.to_payload()
                self.debug_message(f"request data: {payload_data}")
                result = await self._post_request(
                    session=session,
                    endpoint=method.endpoint,
                    json_data=payload_data,
                )
        except ClientError as e:
            raise BadRequestError(e)
        self.debug_message(f"request result: {result}")
        return result


class DefaultApiClient(HttpClient):
    async def get_exchange_rates_all(self) -> GetExchangeRatesResponse:
        """Get all exchange rates, https://apidocs.bitpapa.com/docs/backend-apis-english/97573257c4827-get-a-v-1-exchange-rate-all

        Returns:
            GetExchangeRatesOut: An object where the keys are abbreviations of
            a pair of exchange rates separated by "_"
        """
        method = GetExchangeRateMetod()
        result = await self._make_request(method)
        return GetExchangeRatesResponse(**result)

    async def get_withdrawal_fees(self) -> GetWithdrawalFeesResponse:
        """
        Список слоев комиссий за вывод BTC и XMR в зависимости от суммы вывода в USD.
        """
        method = GetWithdrawalFeesMethod()
        result = await self._make_request(method)
        return GetWithdrawalFeesResponse(**result)


class AdressesApiClient(HttpClient):
    async def get_addresses(
        self,
        currency: Optional[str] = None,
        label: Optional[str] = None,
    ) -> GetAddressesResponse:
        method = GetAddressesMethod(currency=currency, label=label)
        result = await self._make_request(method)
        return GetAddressesResponse(addresses=result)

    async def create_address(
        self,
        currency: str,
        network: str,
        label: str = "",
    ) -> CreateAddressResponse:
        method = CreateAddressMethod(
            currency=currency,
            network=network,
            label=label,
        )
        result = await self._make_request(method)
        return CreateAddressResponse(**result)

    async def get_transactions(
        self,
        page: int = 1,
        limit: int = 100,
    ) -> GetTransactionsResponse:
        method = GetTransactionsMethod(page=page, limit=limit)
        result = await self._make_request(method)
        return GetTransactionsResponse(transactions=result)

    async def get_address_transactions(
        self,
        uuid: str,
        page: int = 1,
        limit: int = 100,
    ) -> GetAddressTransactionsResponse:
        method = GetAddressTransactionMethod(
            uuid=uuid,
            page=page,
            limit=limit,
        )
        result = await self._make_request(method)
        return GetAddressTransactionsResponse(**result)

    async def create_transaction(
        self,
        currency: str,
        amount: float,
        from_address: str,
        to_address: str,
        network: str,
        label: str = "",
    ) -> TransactionResponse:
        method = CreateTransactionMethod(
            currency=currency,
            amount=amount,
            from_address=from_address,
            to_address=to_address,
            network=network,
            label=label,
        )
        result = await self._make_request(method)
        return TransactionResponse(**result)

    async def master_withdrawal_transaction(
        self,
        currency: str,
        amount: float,
        to_address: str,
        network: str,
        label: str = "",
    ) -> TransactionResponse:
        method = MasterWithdrawalTransactionMethod(
            currency=currency,
            amount=amount,
            to_address=to_address,
            network=network,
            label=label,
        )
        result = await self._make_request(method)
        return TransactionResponse(**result)

    async def master_refill_transaction(
        self,
        currency: str,
        amount: float,
        from_address: str,
        network: str,
        label: str = "",
    ) -> TransactionResponse:
        method = MasterRefillTransactionMethod(
            currency=currency,
            amount=amount,
            from_address=from_address,
            network=network,
            label=label,
        )
        result = await self._make_request(method)
        return TransactionResponse(**result)


class BitpapaPayClient(HttpClient):
    async def get_invoices(self, page: int = 1) -> GetInvoicesResponse:
        """Get the list of invoices, https://apidocs.bitpapa.com/docs/backend-apis-english/qph49kfhdjx0x-get-the-list-of-invoices

        Returns:
            TelegramInvoices: list of telegram invoices
        """
        method = GetInvoicesMethod(page=page)
        result = await self._make_request(method)
        return GetInvoicesResponse(**result)

    async def create_crypto_invoice(
        self,
        amount: float,
        currency_code: str,
        expiration_time: Optional[int] = None,
        merchant_invoice_id: Optional[str] = None,
        paid_button_name: Optional[str] = None,
        paid_button_url: Optional[str] = None,
        private_message: Optional[str] = None,
        crypto_address: Optional[str] = None,
    ) -> CreateInvoiceResponse:
        method = CreateCryptoInvoiceMethod(
            amount=amount,
            currency_code=currency_code,
            crypto_address=crypto_address,
            expiration_time=expiration_time,
            merchant_invoice_id=merchant_invoice_id,
            paid_button_name=paid_button_name,
            paid_button_url=paid_button_url,
            private_message=private_message,
        )
        raw_response = await self._make_request(method)
        return CreateInvoiceResponse(**raw_response)

    async def create_fiat_invoice(
        self,
        accepted_crypto: List[str],
        fiat_amount: float,
        fiat_currency_code: str,
        expiration_time: Optional[int] = None,
        merchant_invoice_id: Optional[str] = None,
        paid_button_name: Optional[str] = None,
        paid_button_url: Optional[str] = None,
        private_message: Optional[str] = None,
        crypto_address: Optional[str] = None,
    ) -> CreateInvoiceResponse:
        method = CreateFiatInvoiceMethod(
            accepted_crypto=accepted_crypto,
            fiat_amount=fiat_amount,
            fiat_currency_code=fiat_currency_code,
            crypto_address=crypto_address,
            expiration_time=expiration_time,
            merchant_invoice_id=merchant_invoice_id,
            paid_button_name=paid_button_name,
            paid_button_url=paid_button_url,
            private_message=private_message,
        )
        raw_response = await self._make_request(method)
        return CreateInvoiceResponse(**raw_response)


class BitpapaPay(BitpapaPayClient, AdressesApiClient, DefaultApiClient):
    pass
