import datetime
import re
import typing

from smsclient.exceptions import SMSClientError


def raise_for_errors(
    response: dict[str, typing.Any],
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
