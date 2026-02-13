from typing import TypedDict

from pysmscenter.types.base import BaseResponse


class MobileData(TypedDict):
    cost: int
    country: str
    countryCode: int
    gsmCode: str
    mcc: str
    mnc: str
    msisdn: str
    national: str
    number: str


class MobileRawData(BaseResponse, total=False):
    total: int
    mobile: MobileData
