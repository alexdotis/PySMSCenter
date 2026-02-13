from typing import Any

import pytest

from pysmscenter import SMSClient
from pysmscenter.exceptions import CredentialError


class TestBalanceManager:
    def test_balance_check_calls_api(self, client: SMSClient, mocker: Any) -> None:
        fake_response = {
            "status": "1",
            "balance": "2",
            "remarks": "Success",
            "error": "0",
        }

        call_mock = mocker.patch.object(
            client.balance,
            "call",
            return_value=fake_response,
        )

        response = client.balance.check()

        call_mock.assert_called_once_with(
            "GET",
            "me/balance",
        )
        assert response == fake_response

    def test_balance_manager_str(self, client: SMSClient) -> None:
        assert str(client.balance) == "BalanceManager"

    def test_balance_raises_credential_error(self, client: SMSClient, mocker: Any) -> None:
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
            client.balance.check()
        assert exc.value.code == "101"
