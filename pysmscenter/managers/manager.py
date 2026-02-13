from collections.abc import Mapping
from typing import Any, ClassVar, TYPE_CHECKING

if TYPE_CHECKING:
    from pysmscenter.main import SMSClient


class Manager:
    name: ClassVar[str]

    def __init__(self, client: "SMSClient") -> None:
        self.client = client

    def call(
        self,
        method: str,
        endpoint: str,
        params: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        return self.client.fetch_data(method, endpoint, params)
