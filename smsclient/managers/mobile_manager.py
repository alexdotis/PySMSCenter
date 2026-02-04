import typing

from smsclient.exceptions import MobileExceptionError
from smsclient.utils import raise_for_errors

from .manager import Manager


class MobileData(typing.TypedDict):
    cost: int
    country: str
    countryCode: int
    gsmCode: str
    mcc: str
    mnc: str
    msisdn: str
    national: str
    number: str


class MobileRawData(typing.TypedDict, total=False):
    status: typing.Literal["0", "1"]
    error: str
    remarks: str
    total: int
    mobile: MobileData


class MobileManager(Manager):
    name = "mobile"

    def __str__(self) -> str:
        return self.__class__.__name__

    def check(self, mobile: str) -> MobileRawData:
        """Check the mobile number

        Args:
            mobile (str): Mobile number to check

        Raises:
            MobileExceptionError: If error code is in error_codes

        Returns:
            MobileRawData: Response from the API
        """
        params = {"mobile": mobile}
        response = self.call("GET", "mobile/check", params)
        raise_for_errors(response, MobileExceptionError)

        return typing.cast(MobileRawData, response)
