from typing import Any, Literal, Optional

from pydantic import BaseModel


class BaseOutData(BaseModel):
    endpoint: str
    request_type: Literal["GET", "POST"]
    params: Optional[dict] = None
    json_data: Optional[dict] = None
    returning_model: Any
