# Bitpapa Pay asynchronous api wrapper

**Docs**: https://apidocs.bitpapa.com/docs/apidocs/wvea40l9be95f-integracziya-bitpapa-pay

## Installation

Install bitpapa-pay

```
pip install bitpapa-pay
```

## Usage/Examples

```python
import asyncio

from bitpapa_pay import BitpapaPay


async def main():
    bitpapa_pay = BitpapaPay(api_token="api_token")
    # Создаем крипто инвойс
    crypto_invoice = await bitpapa_pay.create_crypto_invoice(
        amount=1, currency_code="USDT",
        private_message="test crypto invoice message",
        paid_button_name="open_bot",
        paid_button_url="https://google.com"
    )
    print(crypto_invoice)

    # Создаем фиат инвойс
    fiat_invoice = await bitpapa_pay.create_fiat_invoice(
        accepted_crypto=["USDT"],
        fiat_amount=10,
        fiat_currency_code="RUB",
        expiration_time=29,
        merchant_invoice_id="test merchant id 123",
        paid_button_name="callback",
        paid_button_url="https://google.com",
        private_message="test fiat invoice message"
    )
    print(fiat_invoice)

    # Получаем инвойсы
    invoices = await bitpapa_pay.get_invoices(page=3)
    print(invoices)

    await bitpapa_pay.close()


if __name__ == "__main__":
    asyncio.run(main())
```
