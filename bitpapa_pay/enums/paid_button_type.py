from enum import Enum


class PaidButtonType(str, Enum):
    GET_ITEM = "get_item"
    OPEN_CHANNEL = "open_channel"
    OPEN_BOT = "open_bot"
    OPEN_STORE = "open_store"
    CALLBACK = "callback"