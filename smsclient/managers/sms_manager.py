import typing

from .manager import Manager


class SMSExceptionError(Exception):
    pass


class SMSRawData(typing.TypedDict):
    status: str
    id: str
    cost: str
    balance: str
    mcc: str
    mnc: str
    remarks: str
    error: str


class SMSCancelRawData(typing.TypedDict):
    smsId: str
    status: str
    remarks: str
    error: str


class SmsManager(Manager):
    name = "sms"

    def __str__(self) -> str:  # type: ignore
        return self.__class__.__name__

    def send(self, to: str, text: str, sender: str, **kwargs) -> SMSRawData:
        """Send an SMS

        Args:
            to (str): Mobile of recipent. [Required]
            text (str): Text of the sms to send_
            sender (str): Sender of the sms

        Raises:
            SMSExceptionError: if error code is in error_codes

        Returns:
            dict[str, typing.Any]: Response from the API
        """
        params = {"to": to, "text": text, "from": sender, "type": "json", **kwargs}

        response = self.call("GET", "sms/send", params)
        error_codes = {"102", "103", "104", "105", "106"}

        if response.get("error") in error_codes:
            raise SMSExceptionError(response.get("remarks"))

        return typing.cast(SMSRawData, response)

    def bulk(
        self, to: typing.Sequence[str], text: str, sender: str, **kwargs
    ) -> dict[str, typing.Any]:
        """Send an SMS to multiple recipients
        Args:
            to (typing.Sequence[str]): multiple mobiles to send the sms to
            text (str): Text of the sms to send
            sender (str): Sender of the sms

        Raises:
            SMSExceptionError: if error code is in error_codes

        Returns:
            dict[str, typing.Any]: Response from the API
        """

        if isinstance(to, list):
            to = ",".join(to)

        params = {"to": to, "text": text, "from": sender, "type": "json", **kwargs}

        response = self.call("GET", "sms/bulk", params)
        error_codes = {"102", "103", "104", "105", "106"}

        if response.get("error") in error_codes:
            raise SMSExceptionError(response.get("remarks"))

        return response

    def cancel(self, sms_id: str) -> SMSCancelRawData:
        """Cancel an SMS

        Args:
            sms_id (str): ID of the sms to cancel

        Returns:
            SMSCancelRawData: Response from the API
        """
        params = {"smsId": sms_id, "type": "json"}
        response = self.call("GET", "sms/cancel", params)
        return typing.cast(SMSCancelRawData, response)
