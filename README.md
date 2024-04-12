
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
    result = await bitpapa_pay.create_invoice("USDT", 100)
    print(result.model_dump())
    print(
        result.invoice.id,
        result.invoice.currency_code,
        result.invoice.amount,
        result.invoice.status,
        result.invoice.created_at,
        result.invoice.updated_at,
        result.invoice.url
    )
    result = await bitpapa_pay.get_invoices()
    for invoice in result.invoices:
        print(
            invoice.id,
            invoice.currency_code,
            invoice.amount,
            invoice.status,
            invoice.created_at,
            invoice.updated_at,
            invoice.url
        )
    result = await bitpapa_pay.get_exchange_rates_all()
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
```

