from typing import cast

from pysmscenter.types import PurchaseRawResponse

from .manager import Manager


class PurchaseManager(Manager):
    name = "purchase"

    def __str__(self) -> str:
        return self.__class__.__name__

    def list(self) -> PurchaseRawResponse:
        """List available purchase options.

        Returns:
            PurchaseRawResponse: Response from the API.
        """
        response = self.call("GET", "purchase/list")

        return cast(PurchaseRawResponse, response)
