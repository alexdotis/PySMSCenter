from typing import TypeAlias, TypedDict


class StatusItem(TypedDict, total=False):
    id: str
    smsId: str
    status: str
    cost: str
    ttd: str


StatusRawResponse: TypeAlias = dict[str, StatusItem | str]
