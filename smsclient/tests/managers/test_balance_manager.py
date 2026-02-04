from typing import Any

from smsclient import SMSClient


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
            {"type": "json"},
        )
        assert response == fake_response

    def test_balance_manager_str(self, client: SMSClient) -> None:
        assert str(client.balance) == "BalanceManager"
