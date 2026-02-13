from typing import Any

import pytest

from pysmscenter import SMSClient
from pysmscenter.exceptions import HLRExceptionError


class TestHlrManager:
    def test_success_lookup(self, client: SMSClient, mocker: Any) -> None:
        fake_response = {
            "result": "OK",
            "description": "The request was successful",
            "mcc": "202",
            "mnc": "01",
            "network": "Telestet",
            "country": "GREECE",
            "countryCode": "30",
            "ported": "no",
            "cctld": "el",
            "mccInitial": "202",
            "mncInitial": "01",
            "status": "1",
            "remarks": "Success",
            "error": "0",
        }

        call_mock = mocker.patch.object(client.hlr, "call", return_value=fake_response)

        response = client.hlr.lookup("6912345678")

        call_mock.assert_called_once_with(
            "GET",
            "hlr/lookup",
            params={"mobile": "6912345678"},
        )
        assert response == fake_response

    @pytest.mark.parametrize(
        ("error_code", "error_response"),
        [
            ("105", "Error: Account out of balane"),
            ("201", "Error: Failed to parse mobile to MSISDN"),
            ("205", "Error: No [mobile] parameter"),
        ],
    )
    def test_lookup_with_error(self, client: SMSClient, mocker: Any, error_code: str, error_response: str) -> None:
        fake_response = {
            "status": "0",
            "error": error_code,
            "remarks": error_response,
        }

        call_mock = mocker.patch.object(client.hlr, "call", return_value=fake_response)

        with pytest.raises(HLRExceptionError) as exc:
            client.hlr.lookup("6912345678")

        call_mock.assert_called_once_with(
            "GET",
            "hlr/lookup",
            params={"mobile": "6912345678"},
        )
        assert exc.value.code == error_code
        assert exc.value.args[0]
