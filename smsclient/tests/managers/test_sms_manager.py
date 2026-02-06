import re
from typing import Any

import pytest

from smsclient import SMSClient
from smsclient.exceptions import SMSExceptionError


class TestSMSManager:
    def test_send_sms_success(self, client: SMSClient, mocker: Any):
        fake_response = {
            "status": "1",
            "id": "123456",
            "cost": "1",
            "balance": "11",
            "mcc": "202",
            "mnc": "01",
            "remarks": "Success: Accepted for delivery",
            "error": "0",
        }

        call_mock = mocker.patch.object(
            client.sms,
            "call",
            return_value=fake_response,
        )

        response = client.sms.send(
            to="6912345678",
            text="Test message",
            sender="SMSCenter",
        )

        call_mock.assert_called_once_with(
            "GET",
            "sms/send",
            {
                "to": "6912345678",
                "text": "Test message",
                "from": "SMSCenter",
                "type": "json",
            },
        )

        assert response == fake_response

    @pytest.mark.parametrize(
        ("error_code", "error_response"),
        [
            ("102", "Error: Parameter [to] is missing"),
            ("103", "Error: Parameter [to] cannot be parsed"),
            ("104", "Error: Parameter [text] is missing"),
            ("105", "Error: You dont have enough sms"),
            ("106", "Error: Message couldnt be sent"),
        ],
    )
    def test_send_sms_raises_on_error_codes(
        self,
        client: SMSClient,
        error_code: str,
        error_response: str,
        mocker: Any,
    ):
        fake_response = {
            "status": "0",
            "id": "0",
            "cost": "0",
            "balance": "1",
            "mcc": "",
            "mnc": "",
            "remarks": error_response,
            "error": error_code,
        }
        mocker.patch.object(
            client.sms,
            "call",
            return_value=fake_response,
        )
        with pytest.raises(SMSExceptionError, match=re.escape(error_response)) as exc:
            client.sms.send(
                to="6912345678",
                text="Test message",
                sender="SMSCenter",
            )
        assert exc.value.code == error_code
        assert exc.value.args[0]

    def test_sms_bulk_success(self, client: SMSClient, mocker: Any):
        fake_response = {
            "status": "1",
            "id": ["123", "124"],
            "sms": [
                {"id": "123", "smsId": "123", "msisdn": "306900000001"},
                {"id": "124", "smsId": "124", "msisdn": "306900000002"},
            ],
            "balance": "11",
            "cost": "2",
            "accepted": "2",
            "rejected": "0",
            "remarks": "Success",
            "error": "0",
        }

        call_mock = mocker.patch.object(
            client.sms,
            "call",
            return_value=fake_response,
        )

        response = client.sms.bulk(
            to=["6912345678", "6912345679"],
            text="Bulk test",
            sender="SMSCenter",
        )

        call_mock.assert_called_once_with(
            "GET",
            "sms/bulk",
            {
                "to": "6912345678,6912345679",
                "text": "Bulk test",
                "from": "SMSCenter",
                "type": "json",
            },
        )

        assert response == fake_response

    @pytest.mark.parametrize(
        ("error_code", "error_response"),
        [
            ("102", "Error: Parameter [to] is missing"),
            ("103", "Error: Parameter [to] cannot be parsed"),
            ("104", "Error: Parameter [text] is missing"),
            ("105", "Error: You dont have enough sms"),
            ("106", "Error: Message couldnt be sent"),
        ],
    )
    def test_sms_bulk_raises_on_error_codes(
        self,
        client: SMSClient,
        error_code: str,
        error_response: str,
        mocker: Any,
    ):
        fake_response = {
            "status": "0",
            "id": ["0"],
            "sms": [],
            "balance": "1",
            "cost": "0",
            "accepted": "0",
            "rejected": "0",
            "remarks": error_response,
            "error": error_code,
        }
        mocker.patch.object(
            client.sms,
            "call",
            return_value=fake_response,
        )
        with pytest.raises(SMSExceptionError, match=re.escape(error_response)) as exc:
            client.sms.bulk(
                to=["6912345678", "6912345679"],
                text="Bulk test",
                sender="SMSCenter",
            )
        assert exc.value.code == error_code
        assert exc.value.args[0]

    def test_sms_bulk_partial_rejection_does_not_raise(self, client: SMSClient, mocker: Any):
        fake_response = {
            "status": "1",
            "id": ["123"],
            "sms": [
                {"id": "123", "smsId": "123", "msisdn": "306900000001"},
            ],
            "balance": "11",
            "cost": "1",
            "accepted": "1",
            "rejected": "1",
            "remarks": "Success: Accepted for delivery: 1, Not accepted for delivery: 1",
            "error": "0",
        }

        mocker.patch.object(client.sms, "call", return_value=fake_response)

        response = client.sms.bulk(
            to=["6912345678", "invalid"],
            text="Bulk test",
            sender="SMSCenter",
        )

        assert response == fake_response

    @pytest.mark.parametrize(
        ("accepted", "rejected", "expected_sms_len"),
        [
            ("2", "0", 2),
            ("1", "1", 1),
            ("0", "2", 0),
        ],
    )
    def test_sms_bulk_counts(self, client: SMSClient, mocker: Any, accepted, rejected, expected_sms_len):
        fake_response = {
            "status": "1",
            "id": ["123"] * int(accepted),
            "sms": [{"id": "123", "smsId": "123", "msisdn": "306900000001"}] * int(accepted),
            "balance": "11",
            "cost": accepted,
            "accepted": accepted,
            "rejected": rejected,
            "remarks": "Success",
            "error": "0",
        }
        mocker.patch.object(client.sms, "call", return_value=fake_response)

        response = client.sms.bulk(
            to=["a", "b"],
            text="Bulk test",
            sender="SMSCenter",
        )

        assert response["status"] == "1"
        assert response["error"] == "0"
        assert int(response["accepted"]) + int(response["rejected"]) == 2
        assert len(response["sms"]) == expected_sms_len

    def test_cancel_sms_success(self, client: SMSClient, mocker: Any):
        fake_response = {
            "status": "1",
            "id": "123",
            "smsId": "123",
            "balance": "8",
            "remarks": "Success: Message purged",
            "error": "0",
        }

        call_mock = mocker.patch.object(
            client.sms,
            "call",
            return_value=fake_response,
        )
        response = client.sms.cancel("123")
        call_mock.assert_called_once_with(
            "GET",
            "sms/cancel",
            {
                "smsId": "123",
                "type": "json",
            },
        )
        assert response == fake_response

    @pytest.mark.parametrize(
        ("error_code", "error_response"),
        [
            ("107", "Error: Parameter smsId is missing"),
            ("108", "Error: Parameter smsId cannot be parsed"),
            ("109", "Error: Message cannot be found"),
            ("110", "Error: Message already delivered or canceled"),
            ("111", "Error: Message couldnt be canceled"),
        ],
    )
    def test_cancel_sms_raises_on_error_codes(
        self,
        client: SMSClient,
        error_code: str,
        error_response: str,
        mocker: Any,
    ):
        fake_response = {
            "status": "0",
            "id": "0",
            "smsId": "0",
            "balance": "1",
            "remarks": error_response,
            "error": error_code,
        }
        mocker.patch.object(
            client.sms,
            "call",
            return_value=fake_response,
        )
        with pytest.raises(SMSExceptionError, match=re.escape(error_response)) as exc:
            client.sms.cancel("123")
        assert exc.value.code == error_code
        assert exc.value.args[0]
