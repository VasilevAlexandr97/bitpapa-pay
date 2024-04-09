from typing import Any, Final, Optional

from aiohttp import ClientSession

from bitpapa_pay.methods.base import BaseMethod
from bitpapa_pay.methods.exchange_rates import (GetExchangeRates,
                                                GetExchangeRatesOut)
from bitpapa_pay.methods.telegram import (CreateTelegramInvoice,
                                          CreateTelegramInvoiceOut,
                                          GetTelegramInvoices,
                                          TelegramInvoices)
from bitpapa_pay.version import VERSION


class HttpClient:
    def __init__(self):
        self.base_url = "https://bitpapa.com"
        self._session: Optional[ClientSession] = None

    def get_session(self):
        if isinstance(self._session, ClientSession):
            return self._session
        self._session = ClientSession(base_url=self.base_url)
        return self._session

    def get_headers(self):
        return {
            "Content-Type": "application/json",
            "User-Agent": f"AioBitpapaPay/{VERSION}"

        }

    async def close(self):
        if isinstance(self._session, ClientSession):
            await self._session.close()

    async def _get_request(
        self,
        session: ClientSession,
        endpoint: str,
        headers: Optional[dict] = None,
        params: Optional[dict] = None
    ):
        async with session.get(
            url=endpoint, headers=headers, params=params
        ) as resp:
            return await resp.json()

    async def _post_request(
        self,
        session: ClientSession,
        endpoint: str,
        headers: Optional[dict] = None,
        json_data: Optional[dict] = None
    ):
        async with session.post(
            url=endpoint, headers=headers, json=json_data
        ) as resp:
            return await resp.json()

    async def _make_request(self, method: BaseMethod):
        headers = self.get_headers()
        request_data = method.get_data()
        session = self.get_session()
        if request_data.request_type == "GET":
            result = await self._get_request(
                session=session,
                endpoint=request_data.endpoint,
                headers=headers,
                params=request_data.params
            )
        elif request_data.request_type == "POST":
            result = await self._post_request(
                session=session,
                endpoint=request_data.endpoint,
                headers=headers,
                json_data=request_data.json_data
            )
        return result


class DefaultApiClient(HttpClient):
    async def get_exchange_rates_all(self) -> GetExchangeRatesOut:
        method = GetExchangeRates()
        result = await self._make_request(method)
        return method.returning_model(**result)


class TelegramBitpapaPay(DefaultApiClient):
    def __init__(self, api_token: str):
        super().__init__()
        self._api_token = api_token

    async def get_invoices(self) -> TelegramInvoices:
        method = GetTelegramInvoices(api_token=self._api_token)
        result = await self._make_request(method)
        return method.returning_model(**result)

    async def create_invoice(
        self,
        currency_code: str,
        amount: int
    ) -> CreateTelegramInvoiceOut:
        method = CreateTelegramInvoice(
            api_token=self._api_token,
            currency_code=currency_code,
            amount=amount
        )
        result = await self._make_request(method)
        return method.returning_model(**result)
