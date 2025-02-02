import typing

from .manager import Manager


class SmS(typing.TypedDict):
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


class SingleListHistoryRawData(typing.TypedDict):
    status: str
    remarks: str
    error: str
    total: str
    sms: list[SmS]


class HistoryManager(Manager):
    name = "history"

    def __str__(self) -> str:  # type: ignore
        return self.__class__.__name__

    def group_list(self) -> None:
        # TODO implement the group list
        raise NotImplementedError

    def single_list(self) -> SingleListHistoryRawData:
        response = self.call("GET", "history/single/list", {"type": "json"})

        return typing.cast(SingleListHistoryRawData, response)
