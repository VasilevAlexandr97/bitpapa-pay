import asyncio
from typing import Any, Final, Optional, Union

from aiohttp import ClientSession
from loguru import logger

from bitpapa_pay import types
from bitpapa_pay.clients.base import Client
from bitpapa_pay.const import VERSION
from bitpapa_pay.methods import (BaseMethod, CreateTelegramInvoice,
                                 GetExchangeRatesAll, GetTelegramInvoices,
                                 TelegramInvoice)

DEFAULT_URL: Final[str] = "https://bitpapa.com"


class BitpapaPay(Client):
    def __init__(self, api_token: str, timeout: Optional[float] = None) -> None:
        """_summary_

        Args:
            api_token (str): api_token from wallet -> https://t.me/bitpapa_bot
            timeout (float | None, optional): request timeout. 
            Defaults to 60.0s.
        """
        super().__init__(timeout)
        self.api_token = api_token
        self._default_url = DEFAULT_URL
        self._session = self._create_session()

    def _create_session(self):
        _session = ClientSession(
            base_url=self._default_url,
            headers={"User-Agent": f"AioBitpapaPay/{VERSION}"}
        )
        return _session

    async def close(self):
        """Close the session and wait for it to be closed."""
        if self._session.closed:
            return

        await self._session.close()
        await asyncio.sleep(0.25)

    async def __call__(self, method) -> Any:
        return await self.make_request(method)

    async def get_request(
        self,
        endpoint: str,
        params: Optional[dict] = None
    ):
        async with self._session.get(
            url=endpoint, params=params, timeout=self.timeout
        ) as response:
            logger.debug(f"RESPONSE URL:{response.url}")
            logger.debug(f"GET RESPONSE STATUS: {response.status}")
            return await self.check_response(response)

    async def post_request(
        self,
        endpoint: str,
        json: Optional[dict] = None
    ):
        async with self._session.post(
            url=endpoint, json=json, timeout=self.timeout
        ) as response:
            logger.debug(f"RESPONSE URL:{response.url}")
            logger.debug(f"POST RESPONSE STATUS: {response.status}")
            return await self.check_response(response)

    async def make_request(self, method: BaseMethod):
        if method._request_type == "GET":
            response = await self.get_request(
                endpoint=method._endpoint,
                params=method.model_dump()
            )
        elif method._request_type == "POST":
            response = await self.post_request(
                endpoint=method._endpoint,
                json=method.model_dump()
            )
        return method._returning(**response)

    async def create_telegram_invoice(
        self,
        currency_code: str,
        amount: Union[int, float]
    ) -> types.TelegramInvoice:
        """Issue an invoice to get payment
        docs url - https://bitpapa.stoplight.io/docs/backend-apis-english/23oj83o5x2su2-issue-an-invoice

        Args:
            currency_code (str): The ticker of accepted cryptocurrency
            amount (int | float): The amount in cryptocurrency

        Returns:
            types.TelegramInvoice: telegram invoice object
        """
        method = CreateTelegramInvoice(
            api_token=self.api_token,
            invoice=TelegramInvoice(
                currency_code=currency_code,
                amount=amount
            )
        )
        return await self(method)

    async def get_telegram_invoices(self) -> types.TelegramInvoices:
        """Get the list of invoices
        docs url - https://bitpapa.stoplight.io/docs/backend-apis-english/qph49kfhdjx0x-get-the-list-of-invoices

        Returns:
            types.TelegramInvoices: list of telegram invoice objects
        """
        method = GetTelegramInvoices(api_token=self.api_token)
        return await self(method)

    async def get_exchange_rates_all(self) -> types.ExchangeRatesAll:
        """Get all exchange rates
        docs url - https://bitpapa.stoplight.io/docs/backend-apis-english/97573257c4827-get-a-v-1-exchange-rate-all
        Returns:
            types.ExchangeRatesAll: An object where the keys are abbreviations of a pair of exchange rates separated by "_"
        """
        method = GetExchangeRatesAll()
        return await self(method)
