import datetime
from typing import TypedDict

from smsclient.types.base import BaseResponse

type Timestamp = int | datetime.datetime


class SMSRawData(BaseResponse):
    id: str
    cost: str
    balance: str
    mcc: str
    mnc: str


class SMSCancelRawData(BaseResponse, total=False):
    smsId: str  # noqa: N815


class SMSBulkItem(TypedDict, total=False):
    id: str
    smsId: str
    msisdn: str


class SMSBulkRawData(BaseResponse, total=False):
    id: list[str]
    sms: list[SMSBulkItem]
    balance: str
    cost: str
    accepted: str
    rejected: str
