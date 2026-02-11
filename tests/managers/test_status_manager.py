import pytest


class TestStatusManager:
    def test_status_get_with_items(self, client, mocker):
        fake_response = {
            "status": "1",
            "remarks": "Success",
            "total": "2",
            "error": "0",
            "0": {"id": "1", "smsId": "1", "status": "d"},
            "1": {"id": "2", "smsId": "2", "status": "s"},
        }

        mocker.patch.object(client.status, "call", return_value=fake_response)

        response = client.status.get()

        assert response["status"] == "1"
        assert response["total"] == "2"

    def test_status_get_empty(self, client, mocker):
        fake_response = {
            "status": "1",
            "remarks": "Info: No pending reports",
            "total": "0",
            "error": "0",
        }

        mocker.patch.object(client.status, "call", return_value=fake_response)

        response = client.status.get()

        assert response["total"] == "0"

    @pytest.mark.parametrize("sms_status", ["d", "s", "f"])
    def test_status_sms(self, client, mocker, sms_status):
        fake_response = {
            "0": {"id": 123, "smsId": 123, "status": sms_status, "cost": "1", "ttd": "4"},
            "sms": {"id": 123, "smsId": 123, "status": sms_status, "cost": "1", "ttd": "4"},
            "status": "1",
            "remarks": "Success",
            "error": "0",
        }

        mocker.patch.object(client.status, "call", return_value=fake_response)

        response = client.status.sms("1")

        assert response["status"] == "1"
        assert response["sms"]["status"] == sms_status
        assert response == fake_response

    def test_status_sms_no_info(self, client, mocker):
        fake_response = {"status": "1", "remarks": "Info: No report", "error": "0"}

        mocker.patch.object(client.status, "call", return_value=fake_response)
        response = client.status.sms("1")
        assert response["status"] == "1"
        assert response["error"] == "0"
