import re
from typing import Any

import pytest

from pysmscenter import SMSClient
from pysmscenter.exceptions import MobileExceptionError


class TestMobileManager:
    def test_mobile_check_calls_api(self, client: SMSClient, mocker: Any) -> None:
        fake_response = {
            "status": "1",
            "remarks": "Success",
            "error": "0",
            "total": 1,
            "mobile": {
                "msisdn": "306912345678",
                "national": "6912345678",
                "country": "GREECE",
                "countryCode": 30,
                "gsmCode": "691",
                "number": "2345678",
                "mcc": "202",
                "mnc": "01",
                "cost": 1,
            },
        }

        call_mock = mocker.patch.object(client.mobile, "call", return_value=fake_response)

        _ = client.mobile.check("6912345678")

        call_mock.assert_called_once_with(
            "GET",
            "mobile/check",
            {"mobile": "6912345678"},
        )

    @pytest.mark.parametrize(
        ("error_code", "error_response"),
        [("201", "Error: Parameter [mobile] cannot be parsed"), ("205", "Error: No [mobile] parameter")],
    )
    def test_mobile_check_raises_on_error_codes(
        self,
        client: SMSClient,
        mocker: Any,
        error_code: str,
        error_response: str,
    ) -> None:
        fake_response = {"status": "0", "remarks": error_response, "error": error_code}

        mocker.patch.object(
            client.mobile,
            "call",
            return_value=fake_response,
        )

        with pytest.raises(MobileExceptionError, match=re.escape(error_response)) as exc:
            client.mobile.check("invalid")

        assert exc.value.code == error_code
        assert exc.value.args[0]

    def test_mobile_manager_str(self, client: SMSClient) -> None:
        assert str(client.mobile) == "MobileManager"
