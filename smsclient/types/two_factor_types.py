from .base import BaseResponse


class TwoFactorRawResponse(BaseResponse, total=False):
    authId: str  #  noqa: N815
    authStatus: str  #  noqa: N815


class TwoFactorCheckResponse(BaseResponse, total=False):
    auth: str
