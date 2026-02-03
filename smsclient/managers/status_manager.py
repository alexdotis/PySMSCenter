import typing

from .manager import Manager


class SmsResponseRawData(typing.TypedDict):
    status: str
    remarks: str
    total: str
    error: str
    items: dict[str, dict[str, str]]


class StatusManager(Manager):
    name = "status"

    def __str__(self) -> str:
        return self.__class__.__name__

    def get(self) -> SmsResponseRawData:
        """Get the status of the sms

        Raises:
            StatusException: If error code is in error_codes

        Returns:
            SmsResponseRawData: Response from the API
        """
        response = self.call("GET", "status/get", {"type": "json"})
        return typing.cast(SmsResponseRawData, response)

    def sms(self, sms_id: str) -> SmsResponseRawData:
        response = self.call("GET", "status/sms", {"smsId": sms_id, "type": "json"})
        return typing.cast(SmsResponseRawData, response)
