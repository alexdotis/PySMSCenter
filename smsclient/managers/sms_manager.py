from collections.abc import Sequence
from typing import cast

from smsclient.exceptions import SMSExceptionError
from smsclient.types import SMSBulkRawData, SMSCancelRawData, SMSRawData, Timestamp
from smsclient.utils import bool2str, raise_for_errors, ts2epoch

from .manager import Manager


class SmsManager(Manager):
    name = "sms"

    def __str__(self) -> str:
        return self.__class__.__name__

    def send(
        self,
        to: str,
        text: str,
        sender: str,
        ucs: bool | None = None,
        flash: bool | None = None,
        timestamp: Timestamp | None = None,
        callback: str | None = None,
    ) -> SMSRawData:
        """Send an SMS.

        Args:
            to (str): Mobile number to send the sms to
            text (str): Text of the sms to send
            sender (str): Sender of the sms
            ucs (bool, optional): Whether the sms is unicode. Defaults to None.
            flash (bool, optional): Whether the sms is flash. Defaults to None.
            timestamp (Timestamp, optional): Timestamp for scheduled sending. Defaults to None.
            callback (str, optional): Callback URL for delivery reports. Defaults to None.

        Raises:
            SMSExceptionError: If the API response indicates an error.

        Returns:
            SMSRawData: Response from the API.
        """
        params = {
            "to": to,
            "text": text,
            "from": sender,
            "ucs": bool2str(ucs) if ucs is not None else None,
            "flash": bool2str(flash) if flash is not None else None,
            "timestamp": ts2epoch(timestamp) if timestamp is not None else None,
            "callback": callback,
        }
        params = {key: value for key, value in params.items() if value is not None}

        response = self.call("GET", "sms/send", params)

        raise_for_errors(response, SMSExceptionError)

        return cast(SMSRawData, response)

    def bulk(
        self,
        to: Sequence[str] | str,
        text: str,
        sender: str,
        ucs: bool | None = None,
        flash: bool | None = None,
        timestamp: Timestamp | None = None,
    ) -> SMSBulkRawData:
        """Send an SMS to multiple recipients.

        Args:
            to (Sequence[str] | str): multiple mobiles to send the sms to
            text (str): Text of the sms to send
            sender (str): Sender of the sms
            ucs (bool, optional): Whether the sms is unicode. Defaults to None.
            flash (bool, optional): Whether the sms is flash. Defaults to None.
            timestamp (Timestamp, optional): Timestamp for scheduled sending. Defaults to None.

        Raises:
            SMSExceptionError: If the API response indicates an error.

        Returns:
            SMSBulkRawData: Response from the API.
        """

        if isinstance(to, list | tuple):
            to = ",".join(to)

        params = {
            "to": to,
            "text": text,
            "from": sender,
            "ucs": bool2str(ucs) if ucs is not None else None,
            "flash": bool2str(flash) if flash is not None else None,
            "timestamp": ts2epoch(timestamp) if timestamp is not None else None,
        }
        params = {key: value for key, value in params.items() if value is not None}

        response = self.call("GET", "sms/bulk", params)
        raise_for_errors(response, SMSExceptionError)

        return cast(SMSBulkRawData, response)

    def cancel(self, sms_id: str) -> SMSCancelRawData:
        """Cancel a scheduled SMS.

        Note:
            Only scheduled (future timestamp) messages can be canceled.
            Immediate messages are usually not cancellable.

        Args:
            sms_id (str): ID of the sms to cancel

        Raises:
            SMSExceptionError: If the API response indicates an error.

        Returns:
            SMSCancelRawData: Response from the API.
        """
        params = {"smsId": sms_id}
        response = self.call("GET", "sms/cancel", params)
        raise_for_errors(response, SMSExceptionError)
        return cast(SMSCancelRawData, response)
