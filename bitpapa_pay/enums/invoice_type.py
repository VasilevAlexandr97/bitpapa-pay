from enum import Enum


class InvoiceType(str, Enum):
    FIAT = "fiat"
    CRYPTO = "crypto"
