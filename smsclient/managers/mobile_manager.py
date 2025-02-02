import typing

from .manager import Manager


class MobileExceptionError(Exception):
    pass


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


class MobileRawData(typing.TypedDict):
    error: str
    mobile: MobileData
    remarks: str
    status: str
    total: int


class MobileManager(Manager):
    name = "mobile"

    def __str__(self) -> str:  # type: ignore
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
        error_codes = {"201", "205"}
        params = {"mobile": mobile}
        response = self.call("GET", "mobile/check", params)
        if response.get("error") in error_codes:
            raise MobileExceptionError(response.get("remarks"))
        return typing.cast(MobileRawData, response)
