from typing import Optional, Union

from aiohttp import ClientSession
from loguru import logger

from bitpapa_pay.methods.addresses import (CreateAddress,
                                           CreateAddressOutputData,
                                           GetAddresses,
                                           GetAddressesOutputData,
                                           GetAddressTransactions,
                                           GetTransactions,
                                           GetTransactionsOutputData)
from bitpapa_pay.methods.base import BaseMethod
from bitpapa_pay.methods.exchange_rates import (GetExchangeRates,
                                                GetExchangeRatesOut)
from bitpapa_pay.methods.telegram import (CreateTelegramInvoice,
                                          CreateTelegramInvoiceOutputData,
                                          GetTelegramInvoices,
                                          TelegramInvoices)
from bitpapa_pay.version import VERSION


class HttpClient:
    def __init__(self, api_token: str, debug: bool = False) -> None:
        self._debug = debug
        self._base_url = "https://bitpapa.com"
        self._api_token = api_token
        self._session: Optional[ClientSession] = None

    def debug_message(self, message: str):
        if self._debug:
            logger.debug(message)

    def get_headers(self):
        return {
            "Content-Type": "application/json",
            "User-Agent": f"AioBitpapaPay/{VERSION}",
            "X-Access-Token": self._api_token
        }

    def get_session(self) -> ClientSession:
        headers = self.get_headers()
        self.debug_message(f"request headers: {headers}")

        if isinstance(self._session, ClientSession):
            return self._session
        self._session = ClientSession(base_url=self._base_url, headers=headers)
        return self._session

    async def close(self):
        if isinstance(self._session, ClientSession):
            await self._session.close()

    async def _get_request(
        self,
        session: ClientSession,
        endpoint: str,
        params: Optional[dict] = None
    ):
        async with session.get(url=endpoint, params=params) as resp:
            return await resp.json()

    async def _post_request(
        self,
        session: ClientSession,
        endpoint: str,
        json_data: Optional[dict] = None
    ):
        async with session.post(url=endpoint, json=json_data) as resp:
            return await resp.json()

    async def _make_request(self, method: BaseMethod):
        session = self.get_session()
        request_data = method.get_data()
        self.debug_message(f"request data: {request_data}")
        self.debug_message(
            f"request url: {self._base_url}{request_data.endpoint}"
        )
        if request_data.request_type == "GET":
            result = await self._get_request(
                session=session,
                endpoint=request_data.endpoint,
                params=request_data.params
            )
        elif request_data.request_type == "POST":
            result = await self._post_request(
                session=session,
                endpoint=request_data.endpoint,
                json_data=request_data.json_data
            )
        self.debug_message(f"request result: {result}")
        return result


class DefaultApiClient(HttpClient):
    async def get_exchange_rates_all(self) -> GetExchangeRatesOut:
        """Get all exchange rates, https://apidocs.bitpapa.com/docs/backend-apis-english/97573257c4827-get-a-v-1-exchange-rate-all

        Returns:
            GetExchangeRatesOut: An object where the keys are abbreviations of 
            a pair of exchange rates separated by "_"
        """
        method = GetExchangeRates()
        result = await self._make_request(method)
        return method.returning_model(**result)


class AdressesApiClient(HttpClient):
    async def get_addresses(
        self,
        currency: Optional[str] = None,
        label: Optional[str] = None
    ) -> GetAddressesOutputData:
        method = GetAddresses(currency, label)
        result = await self._make_request(method)
        return method.returning_model(addresses=result)

    async def create_address(
        self,
        currency: str,
        network: str,
        label: str = ""
    ) -> CreateAddressOutputData:
        method = CreateAddress(currency, network, label)
        result = await self._make_request(method)
        return method.returning_model(**result)

    async def get_transactions(
        self
    ) -> GetTransactionsOutputData:
        method = GetTransactions()
        result = await self._make_request(method)
        return method.returning_model(transactions=result)

    async def get_address_transactions(
        self,
        uuid: str
    ) -> GetTransactionsOutputData:
        method = GetAddressTransactions(uuid)
        result = await self._make_request(method)
        return method.returning_model(**result)


class BitpapaPayClient(HttpClient):
    async def get_invoices(self) -> TelegramInvoices:
        """Get the list of invoices, https://apidocs.bitpapa.com/docs/backend-apis-english/qph49kfhdjx0x-get-the-list-of-invoices

        Returns:
            TelegramInvoices: list of telegram invoices
        """
        method = GetTelegramInvoices(api_token=self._api_token)
        result = await self._make_request(method)
        return method.returning_model(**result)

    async def create_invoice(
        self,
        currency_code: str,
        amount: Union[int, float],
        crypto_address: Optional[str] = None
    ) -> CreateTelegramInvoiceOutputData:
        """Issue an invoice to get payment, https://apidocs.bitpapa.com/docs/backend-apis-english/23oj83o5x2su2-issue-an-invoice
        Args:
            currency_code (str): The ticker of accepted cryptocurrency, example: USDT
            amount (Union[int, float]): The amount in cryptocurrency, example 100

        Returns:
            CreateTelegramInvoiceOutputData: Created telegram invoice data
        """
        method = CreateTelegramInvoice(
            api_token=self._api_token,
            currency_code=currency_code,
            amount=amount,
            crypto_address=crypto_address
        )
        result = await self._make_request(method)
        return method.returning_model(**result)


class BitpapaPay(BitpapaPayClient, DefaultApiClient, AdressesApiClient):
    pass
