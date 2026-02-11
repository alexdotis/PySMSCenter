from typing import Any

import pytest

from smsclient import SMSClient
from smsclient.exceptions import CredentialError


class TestKeyManager:
    def test_get_key(self, client: SMSClient, mocker: Any) -> None:
        fake_response = {
            "status": "1",
            "remarks": "Success",
            "key": "fake_api_key_123456",
            "error": "0",
        }

        call_mock = mocker.patch.object(
            client.key,
            "call",
            return_value=fake_response,
        )
        response = client.key.get(username="testuser", password="testpass")  # noqa: S106
        call_mock.assert_called_once_with(
            "GET",
            "key/get",
            params={"username": "testuser", "password": "testpass"},
        )
        assert response == fake_response

    def test_reset_key(self, client: SMSClient, mocker: Any) -> None:
        fake_response = {
            "status": "1",
            "remarks": "Success",
            "key": "new_fake_api_key_654321",
            "error": "0",
        }

        call_mock = mocker.patch.object(
            client.key,
            "call",
            return_value=fake_response,
        )
        response = client.key.reset(username="testuser", password="testpass")  # noqa: S106
        call_mock.assert_called_once_with(
            "GET",
            "key/reset",
            params={"username": "testuser", "password": "testpass"},
        )
        assert response == fake_response

    def test_get_key_raises_credential_error(self, client: SMSClient, mocker: Any) -> None:
        fake_response = {
            "status": "0",
            "remarks": "Invalid API key",
            "error": "101",
        }

        mock_response = mocker.Mock()
        mock_response.json.return_value = fake_response
        mock_response.raise_for_status.return_value = None

        mocker.patch.object(client.session, "request", return_value=mock_response)

        with pytest.raises(CredentialError, match="Invalid API key") as exc:
            client.key.get(username="testuser", password="testpass")  # noqa: S106

        assert exc.value.code == "101"

    def test_reset_key_raises_credential_error(self, client: SMSClient, mocker: Any) -> None:
        fake_response = {
            "status": "0",
            "remarks": "Invalid API key",
            "error": "101",
        }

        mock_response = mocker.Mock()
        mock_response.json.return_value = fake_response
        mock_response.raise_for_status.return_value = None

        mocker.patch.object(client.session, "request", return_value=mock_response)

        with pytest.raises(CredentialError, match="Invalid API key") as exc:
            client.key.reset(username="testuser", password="testpass")  # noqa: S106

        assert exc.value.code == "101"
