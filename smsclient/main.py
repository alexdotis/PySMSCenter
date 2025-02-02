import typing
from contextlib import contextmanager
from urllib.parse import urljoin

from requests import Session
from requests.adapters import HTTPAdapter

from .managers.balance_manager import BalanceManager
from .managers.contact_manager import ContactManager
from .managers.history_manager import HistoryManager
from .managers.mobile_manager import MobileManager
from .managers.sms_manager import SmsManager
from .managers.status_manager import StatusManager


class CrendetialError(Exception):
    pass


@contextmanager
def make_session(max_retries: int) -> typing.Iterator[Session]:
    session = Session()
    adapter = HTTPAdapter(max_retries=max_retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    try:
        yield session
    finally:
        session.close()


class SMSClient:
    BASE_URL = "https://smscenter.gr/api/"
    managers: typing.ClassVar[list] = [
        MobileManager,
        SmsManager,
        BalanceManager,
        HistoryManager,
        StatusManager,
        ContactManager,
    ]

    def __init__(self, api_key: str, max_retries: int = 0) -> None:
        self.api_key = api_key
        self.max_retries = max_retries
        self._setup_managers()

    @property
    def session(self) -> Session:
        if not hasattr(self, "_session"):
            self._session = Session()
            adapter = HTTPAdapter(max_retries=self.max_retries)
            self._session.mount("http://", adapter)
            self._session.mount("https://", adapter)
        return self._session

    def _setup_managers(self) -> None:
        for manager in self.managers:
            setattr(self, manager.name, manager(self))

    def fetch_data(
        self, method: str, endpoint: str, params: dict[str, typing.Any]
    ) -> dict[str, typing.Any]:

        if params.get("api_key") is None:
            params.update({"key": self.api_key})

        url = urljoin(self.BASE_URL, endpoint)

        response = self.session.request(method, url, params)
        response.raise_for_status()
        response_json = response.json()
        self.handle_101_error(response_json)
        return response_json

    def handle_101_error(self, response: dict[str, typing.Any]) -> None:
        if response.get("error") == "101":
            raise CrendetialError(response.get("remarks"))
