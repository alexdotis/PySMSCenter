from typing import TypedDict


class StatusItem(TypedDict, total=False):
    id: str
    smsId: str
    status: str
    cost: str
    ttd: str


type StatusRawResponse = dict[str, StatusItem | str]
