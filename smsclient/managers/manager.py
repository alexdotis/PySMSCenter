import typing
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from smsclient.main import SMSClient


class Manager:
    def __init__(self, client: "SMSClient") -> None:
        self.client = client

    def call(self, method: str, endpoint: str, params: dict[str, typing.Any]) -> dict[str, typing.Any]:
        return self.client.fetch_data(method, endpoint, params)
