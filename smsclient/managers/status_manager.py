import typing

from .manager import Manager


class SmsResponseRawData(typing.TypedDict, total=False):
    status: typing.Literal["0", "1"]
    remarks: str
    total: str
    error: str
    items: dict[str, dict[str, str]]


class StatusManager(Manager):
    name = "status"

    def __str__(self) -> str:
        return self.__class__.__name__

    def get(self) -> SmsResponseRawData:
        """Get delivery statuses for recent messages.

        Returns:
            SmsResponseRawData: Response from the API.
        """
        response = self.call("GET", "status/get", {"type": "json"})
        return typing.cast(SmsResponseRawData, response)

    def sms(self, sms_id: str) -> SmsResponseRawData:
        """Get delivery status for a specific SMS.

        Args:
            sms_id: SMS ID to look up.

        Returns:
            SmsResponseRawData: Response from the API.
        """
        response = self.call("GET", "status/sms", {"smsId": sms_id, "type": "json"})
        return typing.cast(SmsResponseRawData, response)
