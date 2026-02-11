from typing import Any

import pytest

from smsclient import SMSClient
from smsclient.exceptions import TwoFactorExceptionError


class TestTwoFactorManager:
    @pytest.mark.parametrize(
        ("auth_status", "remarks"),
        [
            ("s", "Success: Message sent"),
            ("d", "Success: Message delivered to handset"),
            ("f", "Failure: Message failed to send"),
        ],
    )
    def test_send_success(self, client: SMSClient, mocker: Any, auth_status: str, remarks: str) -> None:
        fake_response = {
            "status": "1",
            "authId": "1234",
            "authStatus": auth_status,
            "remarks": remarks,
            "error": "0",
        }

        call_mock = mocker.patch.object(
            client.two_factor,
            "call",
            return_value=fake_response,
        )

        response = client.two_factor.send(
            to="6912345678",
            text="Your 2FA code is: %%code%%",
        )

        call_mock.assert_called_once_with(
            "GET",
            "2fa/send",
            params={
                "to": "6912345678",
                "text": "Your 2FA code is: %%code%%",
            },
        )

        assert response == fake_response

    @pytest.mark.parametrize(
        ("error_code", "error_message"),
        [
            ("102", "Error: Parameter [to] is missing"),
            ("103", "Error: Invalid mobile number"),
            ("105", "Error: Not enough balance"),
            ("106", "Error: Failed to queue message"),
        ],
    )
    def test_send_error(self, client: SMSClient, mocker: Any, error_code: str, error_message: str) -> None:
        fake_response = {
            "status": "0",
            "remarks": error_message,
            "error": error_code,
        }

        mocker.patch.object(
            client.two_factor,
            "call",
            return_value=fake_response,
        )

        with pytest.raises(TwoFactorExceptionError) as exc_info:
            client.two_factor.send(
                to="6912345678",
                text="Your 2FA code is: %%code%%",
            )

        assert exc_info.value.code == error_code
        assert exc_info.value.args[0]

    @pytest.mark.parametrize(
        ("auth"),
        [
            ("nok"),
            ("ok"),
        ],
    )
    def test_check_success(self, client: SMSClient, mocker: Any, auth: str) -> None:
        fake_response = {"status": "1", "auth": auth, "remarks": "Error: Not authenticated", "error": "0"}
        call_mock = mocker.patch.object(
            client.two_factor,
            "call",
            return_value=fake_response,
        )

        response = client.two_factor.check(auth_id="1234", code="5678")

        call_mock.assert_called_once_with(
            "GET",
            "2fa/check",
            params={
                "authId": "1234",
                "code": "5678",
            },
        )

        assert response == fake_response

    @pytest.mark.parametrize(
        ("error_code", "error_message"),
        [
            ("300", "Error: Parameter [authId] is missing"),
            ("301", "Error: Parameter [code] is missing"),
            ("301", "Error: Invalid authId"),
        ],
    )
    def test_check_error(self, client: SMSClient, mocker: Any, error_code: str, error_message: str) -> None:
        fake_response = {"status": "0", "remarks": error_message, "error": error_code}
        mocker.patch.object(
            client.two_factor,
            "call",
            return_value=fake_response,
        )

        with pytest.raises(TwoFactorExceptionError) as exc:
            client.two_factor.check(auth_id="1234", code="5678")

        assert exc.value.code == error_code
        assert exc.value.args[0]
