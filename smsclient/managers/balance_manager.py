import typing

from .manager import Manager


class BalanceBaseResponse(typing.TypedDict):
    status: typing.Literal["0", "1"]
    error: str
    remarks: str


class BalanceRawData(BalanceBaseResponse, total=False):
    balance: str


class BalanceManager(Manager):
    name = "balance"

    def __str__(self) -> str:
        return self.__class__.__name__

    def check(self) -> BalanceRawData:
        """Check the balance of the account"""
        response = self.call("GET", "me/balance", {"type": "json"})

        return typing.cast(BalanceRawData, response)
