from .base import BaseResponse


class HLRLookupRawResponse(BaseResponse, total=False):
    result: str
    description: str
    mcc: str
    mnc: str
    network: str
    country: str
    countryCode: str  # noqa: N815
    ported: str
    cctld: str
    mccInitial: str  # noqa: N815
    mncInitial: str  # noqa: N815
