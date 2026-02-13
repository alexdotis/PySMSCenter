from typing import cast

from pysmscenter.exceptions import MobileExceptionError
from pysmscenter.types import MobileRawData
from pysmscenter.utils import raise_for_errors

from .manager import Manager


class MobileManager(Manager):
    name = "mobile"

    def __str__(self) -> str:
        return self.__class__.__name__

    def check(self, mobile: str) -> MobileRawData:
        """Check a mobile number.

        Args:
            mobile (str): Mobile number to check

        Raises:
            MobileExceptionError: If the API response indicates an error.

        Returns:
            MobileRawData: Response from the API.
        """
        params = {"mobile": mobile}
        response = self.call("GET", "mobile/check", params)
        raise_for_errors(response, MobileExceptionError)

        return cast(MobileRawData, response)
