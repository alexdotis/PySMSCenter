import datetime

import pytest

from smsclient.exceptions import SMSClientError
from smsclient.utils import bool2str, parse_date, raise_for_errors, ts2epoch


def test_raise_for_errors_does_not_raise_on_success():
    response = {"status": "1", "error": "0"}
    raise_for_errors(response, SMSClientError)


def test_raise_for_errors_raises_with_code_and_message():
    response = {
        "status": "0",
        "error": "123",
        "remarks": "error message",
    }

    with pytest.raises(SMSClientError) as exc:
        raise_for_errors(response, SMSClientError)

    assert exc.value.code == "123"
    assert exc.value.message == "error message"
    assert exc.value.response == response


def test_parse_date_valid():
    d = parse_date("2024-01-05")
    assert d.year == 2024
    assert d.month == 1
    assert d.day == 5


@pytest.mark.parametrize(
    "value",
    [
        "2024/01/05",
        "05-01-2024",
        "20240105",
        "Jan 5 2024",
    ],
)
def test_parse_date_invalid_format(value):
    with pytest.raises(ValueError, match="Invalid date format"):
        parse_date(value)


def test_parse_date_invalid_date():
    with pytest.raises(ValueError, match="Invalid date format"):
        parse_date("2024-02-31")


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (True, "true"),
        (False, "false"),
        (None, None),
    ],
)
def test_bool2str(value, expected):
    assert bool2str(value) == expected


def test_ts2epoch_with_int():
    assert ts2epoch(1700000000) == 1700000000


def test_ts2epoch_with_aware_datetime():
    dt = datetime.datetime(2024, 1, 1, tzinfo=datetime.UTC)
    assert ts2epoch(dt) == int(dt.timestamp())


def test_ts2epoch_with_naive_datetime_assumes_utc():
    dt = datetime.datetime(2024, 1, 1)  # noqa: DTZ001
    epoch = ts2epoch(dt)
    assert epoch == int(dt.replace(tzinfo=datetime.UTC).timestamp())
