from typing import cast

from smsclient.exceptions import HLRExceptionError
from smsclient.types import HLRLookupRawResponse
from smsclient.utils import raise_for_errors

from .manager import Manager


class HLRManager(Manager):
    name = "hlr"

    def __str__(self) -> str:
        return self.__class__.__name__

    def lookup(self, mobile: str) -> HLRLookupRawResponse:
        """
        Perform an HLR lookup for the given mobile number.

        Args:
            mobile (str): The mobile number to look up.

        Returns:
            HLRLookupRawResponse: An object containing the HLR lookup result.
        """
        # Implement the HLR lookup logic here
        response = self.call("GET", "hlr/lookup", params={"mobile": mobile})
        raise_for_errors(response, HLRExceptionError)
        return cast(HLRLookupRawResponse, response)
