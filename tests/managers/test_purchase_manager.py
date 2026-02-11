from typing import Any

from smsclient.main import SMSClient


class TestPurchaseManager:
    def test_purchase_list(self, client: SMSClient, mocker: Any) -> None:
        fake_response = {
            "status": "1",
            "remarks": "Success",
            "error": "0",
            "total": "3",
            "purchases": [
                {"purchaseId": "123", "timestamp": "2024-02-04 10:35:28", "cost": "0", "sms": "10"},
                {"purchaseId": "124", "timestamp": "2024-05-13 10:32:39", "cost": "0", "sms": "5"},
                {"purchaseId": "125", "timestamp": "2024-05-09 10:21:20", "cost": "0", "sms": "5"},
            ],
        }

        call_mock = mocker.patch.object(client.purchase, "call", return_value=fake_response)

        response = client.purchase.list()

        call_mock.assert_called_once_with(
            "GET",
            "purchase/list",
        )

        assert response == fake_response
        assert "purchases" in response
        assert isinstance(response["purchases"], list)
        for purchase in response["purchases"]:
            assert "purchaseId" in purchase
            assert "timestamp" in purchase
            assert "cost" in purchase
            assert "sms" in purchase

    def test_purchase_manager_str(self, client: SMSClient) -> None:
        assert str(client.purchase) == "PurchaseManager"
