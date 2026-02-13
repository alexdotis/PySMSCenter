from typing import cast

from pysmscenter.exceptions import TwoFactorExceptionError
from pysmscenter.types import TwoFactorCheckResponse, TwoFactorRawResponse
from pysmscenter.utils import bool2str, raise_for_errors

from .manager import Manager


class TwoFactorManager(Manager):
    name = "two_factor"

    def __str__(self) -> str:
        return self.__class__.__name__

    def send(
        self,
        to: str,
        text: str | None = None,
        sender: str | None = None,
        wait: int | None = None,
        callback: str | None = None,
        ucs: bool | None = None,
    ) -> TwoFactorRawResponse:
        """
        Send a 2FA code to a mobile number.

        Args:
            to (str): The recipient's mobile number.
            text (str, optional): The text message to send. If not provided, a default message will be used.
            sender (str, optional): The sender ID to use for the message.
            If not provided, the default sender will be used.
            wait (int, optional): The time in seconds to wait for a response.
            If not provided, the default wait time will be used.
            callback (str, optional): A URL to receive delivery reports.
            If not provided, no delivery reports will be sent.
            ucs (bool, optional): Whether to send the message in UCS-2 encoding.
            If not provided, the default encoding will be used.

            Extra:
            Both wait and callback paramters are missing then the call will wait for 10 seconds
            by default for the delivery report.
            If the callback parameter is set, or the wait parameter is 0,
            the call will return immediately and if callback is set it will be called
            as soon as the delivery report arrives.
        """

        params = {
            "to": to,
            "text": text,
            "from": sender,
            "wait": wait,
            "callback": callback,
            "ucs": bool2str(ucs) if ucs is not None else None,
        }

        params = {key: value for key, value in params.items() if value is not None}

        response = self.call("GET", "2fa/send", params=params)
        raise_for_errors(response, TwoFactorExceptionError)
        return cast(TwoFactorRawResponse, response)

    def check(self, auth_id: str, code: str) -> TwoFactorCheckResponse:
        """
        Check the 2FA code for a given auth_id.

        Args:
            auth_id (str): The authentication ID received when sending the 2FA code.
            code (str): The 2FA code to check.
        """

        params = {
            "authId": auth_id,
            "code": code,
        }

        response = self.call("GET", "2fa/check", params=params)
        raise_for_errors(response, TwoFactorExceptionError)
        return cast(TwoFactorCheckResponse, response)
