from typing import cast

from pysmscenter.types import BalanceRawData

from .manager import Manager


class BalanceManager(Manager):
    name = "balance"

    def __str__(self) -> str:
        return self.__class__.__name__

    def check(self) -> BalanceRawData:
        """Check the account balance.

        Returns:
            BalanceRawData: Response from the API.
        """
        response = self.call("GET", "me/balance")

        return cast(BalanceRawData, response)
