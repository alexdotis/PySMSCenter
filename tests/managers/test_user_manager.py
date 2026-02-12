from typing import Any

import pytest

from smsclient import SMSClient
from smsclient.exceptions import UserExceptionError


class TestUserManager:
    def test_add_user(self, client: SMSClient, mocker: Any) -> None:
        fake_response = {
            "status": "1",
            "error": "0",
            "remarks": "User added successfully",
            "user": {"userId": "12345", "email": "fake@hotmail.com"},
        }

        call_mock = mocker.patch.object(client.user, "call", return_value=fake_response)

        response = client.user.add(email="fake@hotmail.com", password="fakepassword")  # noqa: S106

        call_mock.assert_called_once_with(
            "GET",
            "user/add",
            params={"email": "fake@hotmail.com", "password": "fakepassword"},
        )
        assert response == fake_response

    def test_add_user_invalid_email(self, client: SMSClient) -> None:
        with pytest.raises(ValueError, match="Invalid email address: invalid-email") as exc_info:
            client.user.add(email="invalid-email", password="fakepassword")  # noqa: S106

        assert str(exc_info.value) == "Invalid email address: invalid-email"

    @pytest.mark.parametrize(
        ("error_core", "error_message"),
        [
            ("601", "Error: User already exists"),
            ("602", "Error: You have reached the maximum number of sub-accounts allowed"),
        ],
    )
    def test_add_user_api_error(self, client: SMSClient, mocker: Any, error_core: str, error_message: str) -> None:
        fake_response = {
            "status": "0",
            "error": error_core,
            "remarks": error_message,
        }

        mocker.patch.object(client.user, "call", return_value=fake_response)
        with pytest.raises(UserExceptionError) as exc_info:
            client.user.add(email="fake@hotmail.com", password="fakepassword")  # noqa: S106
        assert exc_info.value.code == error_core
        assert exc_info.value.args[0]
