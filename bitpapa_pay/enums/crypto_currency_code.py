from enum import Enum


class CryptoCurrencyCode(str, Enum):
    BTC = "BTC"
    DAI = "DAI"
    ETH = "ETH"
    TON = "TON"
    TRX = "TRX"
    USDC = "USDC"
    USDT = "USDT"
    XMR = "XMR"
