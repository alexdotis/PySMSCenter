from typing import Any

from smsclient.main import SMSClient


class TestHistoryManager:
    def test_history_single_list_empty_list(self, client: SMSClient, mocker: Any) -> None:
        fake_response = {"status": "1", "remarks": "Success", "error": "0", "total": "0"}

        call_mock = mocker.patch.object(
            client.history,
            "call",
            return_value=fake_response,
        )

        response = client.history.single_list()
        call_mock.assert_called_once_with(
            "GET",
            "history/single/list",
        )
        assert response == fake_response

    def test_history_single_list_with_sms(self, client: SMSClient, mocker: Any) -> None:
        fake_response = {
            "status": "1",
            "remarks": "Success",
            "error": "0",
            "total": "3",
            "sms": [
                {
                    "smsId": "1234567890",
                    "sender": "SMSCenter",
                    "flash": "false",
                    "unicode": "false",
                    "to": "6912345678",
                    "text": "Test message",
                    "timestamp": "2024-01-01 12:00:00",
                    "status": "d",  # delivered
                    "cost": "1",
                    "ttd": "3",
                },
                {
                    "smsId": "1234567891",
                    "sender": "SMSCenter",
                    "flash": "false",
                    "unicode": "false",
                    "to": "6912345679",
                    "text": "Test message",
                    "timestamp": "2024-01-01 12:00:01",
                    "status": "s",  # sent
                    "cost": "1",
                    "ttd": "0",
                },
                {
                    "smsId": "1234567892",
                    "sender": "SMSCenter",
                    "flash": "false",
                    "unicode": "false",
                    "to": "6912345680",
                    "text": "Test message",
                    "timestamp": "2024-01-01 12:00:02",
                    "status": "f",  # failed
                    "cost": "1",
                    "ttd": "5",
                },
            ],
        }

        call_mock = mocker.patch.object(
            client.history,
            "call",
            return_value=fake_response,
        )

        response = client.history.single_list()
        call_mock.assert_called_once_with(
            "GET",
            "history/single/list",
        )
        assert response == fake_response

    def test_history_group_list(self, client: SMSClient, mocker: Any) -> None:
        fake_response = {
            "0": {
                "groupId": "123",
                "sender": "TestSender",
                "flash": "false",
                "unicode": "false",
                "timestamp": "2024-01-01 12:00:00",
                "text": "Test message",
                "total": 2,
                "cost": 2,
                "sms": [
                    {
                        "smsId": "123",
                        "contactId": "10001",
                        "to": "306912345678",
                        "status": "d",
                        "cost": "1",
                        "ttd": "3",
                    },
                    {
                        "smsId": "124",
                        "contactId": "10002",
                        "to": "306912345679",
                        "status": "d",
                        "cost": "1",
                        "ttd": "5",
                    },
                ],
            },
            "status": "1",
            "remarks": "Success",
            "error": "0",
            "total": "1",
        }

        call_mock = mocker.patch.object(
            client.history,
            "call",
            return_value=fake_response,
        )

        response = client.history.group_list()
        call_mock.assert_called_once_with(
            "GET",
            "history/group/list",
        )
        assert response == fake_response
