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


class SingleListHistoryRawData(typing.TypedDict, total=False):
    status: typing.Literal["0", "1"]
    remarks: str
    error: str
    total: str
    sms: list[SmS]


class HistoryManager(Manager):
    name = "history"

    def __str__(self) -> str:
        return self.__class__.__name__

    def group_list(self) -> None:
        """Get grouped history list (not implemented)."""
        raise NotImplementedError("Group list endpoint is not implemented yet")

    def single_list(self) -> SingleListHistoryRawData:
        """Get the single (non-grouped) SMS history list.

        Returns:
            SingleListHistoryRawData: Response from the API.
        """
        response = self.call("GET", "history/single/list")

        return typing.cast(SingleListHistoryRawData, response)
