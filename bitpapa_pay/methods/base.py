from typing import Any, Dict

from pydantic import BaseModel, ConfigDict

from bitpapa_pay.enums import RequestType


class BaseMethod(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    endpoint: str
    request_type: RequestType


    def to_payload(self) -> Dict[str, Any]:
        return self.model_dump(
            exclude={"endpoint", "request_type", "api_token"},
            by_alias=True,
        )
    
    def to_params(self) -> Dict[str, Any]:
        params = self.model_dump(
            exclude={"endpoint", "request_type", "json_data"},
            by_alias=True,
        )
        return {k: v for k, v in params.items() if v is not None}
