from typing import TypedDict

from smsclient.types.base import BaseResponse


class SmS(TypedDict, total=False):
    smsId: str
    sender: str
    flash: str
    unicode: str
    to: str
    text: str
    timestamp: str
    status: str
    cost: str
    ttd: str
    contactId: str


class SingleListHistoryRawData(BaseResponse, total=False):
    total: str
    sms: list[SmS]


class HistoryGroupSms(TypedDict, total=False):
    smsId: str
    contactId: str
    to: str
    status: str
    cost: str
    ttd: str


class HistoryGroupItem(TypedDict, total=False):
    groupId: str
    sender: str
    flash: str
    unicode: str
    timestamp: str
    text: str
    total: str
    cost: str
    sms: list[HistoryGroupSms]


type GroupListHistoryRawResponse = dict[str, HistoryGroupItem | str]
