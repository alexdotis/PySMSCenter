from .base import BaseResponse


class KeyRawResponse(BaseResponse, total=False):
    key: str
