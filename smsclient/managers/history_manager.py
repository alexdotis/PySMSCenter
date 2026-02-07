from typing import cast

from smsclient.types import GroupListHistoryRawResponse, SingleListHistoryRawData

from .manager import Manager


class HistoryManager(Manager):
    name = "history"

    def __str__(self) -> str:
        return self.__class__.__name__

    def group_list(self) -> GroupListHistoryRawResponse:
        """
        Get the grouped SMS history list.
        Returns:
            GroupListHistoryRawResponse: Response from the API.

        """
        response = self.call("GET", "history/group/list")
        return cast(GroupListHistoryRawResponse, response)

    def single_list(self) -> SingleListHistoryRawData:
        """Get the single (non-grouped) SMS history list.

        Returns:
            SingleListHistoryRawData: Response from the API.
        """
        response = self.call("GET", "history/single/list")

        return cast(SingleListHistoryRawData, response)
