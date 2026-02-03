import typing


def raise_for_errors(
    response: dict[str, typing.Any],
    error_codes: set[str],
    exc: type[Exception],
) -> None:
    if response.get("error") in error_codes:
        raise exc(response.get("remarks"))
