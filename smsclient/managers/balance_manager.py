import typing

from .manager import Manager


class BalanceRawData(typing.TypedDict):
    status: str
    balance: str
    remarks: str
    error: str


class BalanceManager(Manager):
    name = "balance"

    def __str__(self) -> str:
        return self.__class__.__name__

    def check(self) -> BalanceRawData:
        """Check the balance of the account"""
        response = self.call("GET", "me/balance", {"type": "json"})

        return typing.cast(BalanceRawData, response)
