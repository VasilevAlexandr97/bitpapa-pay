from enum import Enum


class RequestType(str, Enum):
    GET = "GET"
    POST = "POST"
