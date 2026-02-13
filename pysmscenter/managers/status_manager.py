from typing import cast

from pysmscenter.types import StatusRawResponse

from .manager import Manager


class StatusManager(Manager):
    name = "status"

    def __str__(self) -> str:
        return self.__class__.__name__

    def get(self) -> StatusRawResponse:
        """Get delivery statuses for recent messages.

        Returns:
            StatusRawResponse: Response from the API.
        """
        response = self.call("GET", "status/get")
        return cast(StatusRawResponse, response)

    def sms(self, sms_id: str) -> StatusRawResponse:
        """Get delivery status for a specific SMS.

        Args:
            sms_id: SMS ID to look up.

        Returns:
            StatusRawResponse: Response from the API.
        """
        response = self.call("GET", "status/sms", {"smsId": sms_id})
        return cast(StatusRawResponse, response)
