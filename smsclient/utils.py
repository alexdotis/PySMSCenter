import datetime
import re
from typing import Any

from smsclient.exceptions import SMSClientError


def raise_for_errors(
    response: dict[str, Any],
    exc: type[SMSClientError],
) -> None:
    if response.get("status") == "0":
        code = str(response.get("error", "")) or None
        remarks = response.get("remarks", "") or None
        raise exc(message=remarks, code=code, response=response)


_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def parse_date(value: str) -> datetime.date:
    if not _DATE_RE.fullmatch(value):
        raise ValueError(f"Invalid date format: {value}. Expected YYYY-MM-DD")

    try:
        return datetime.date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"Invalid date format: {value}. Expected YYYY-MM-DD") from exc


def bool2str(value: bool | None) -> str | None:
    if value is None:
        return None
    return "true" if value else "false"


def ts2epoch(value: int | datetime.datetime) -> int:
    if isinstance(value, int):
        return value
    if value.tzinfo is None:
        value = value.replace(tzinfo=datetime.UTC)
    return int(value.timestamp())
