import types
import typing
from urllib.parse import urljoin

from requests import Session
from requests.adapters import HTTPAdapter

from .exceptions import CrendetialError
from .managers.balance_manager import BalanceManager
from .managers.contact_manager import ContactManager
from .managers.history_manager import HistoryManager
from .managers.mobile_manager import MobileManager
from .managers.sms_manager import SmsManager
from .managers.status_manager import StatusManager
from .utils import raise_for_errors


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
        if not api_key:
            raise CrendetialError("API key is required")
        self.max_retries = max_retries
        self._session: Session | None = None
        self._closed: bool = False

        self._setup_managers()

    def __repr__(self) -> str:
        return f"<SMSClient base_url={self.BASE_URL!r}>"

    @property
    def session(self) -> Session:
        if self._closed:
            raise RuntimeError("Session is closed")

        if self._session is None:
            session = Session()
            adapter = HTTPAdapter(max_retries=self.max_retries)
            session.mount("http://", adapter)
            session.mount("https://", adapter)
            self._session = session
        return self._session

    def close(self) -> None:
        if self._session is not None:
            self._session.close()
            self._session = None
        self._closed = True

    def __enter__(self) -> "SMSClient":
        _ = self.session
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: types.TracebackType | None,
    ) -> bool:
        self.close()
        return False

    def _setup_managers(self) -> None:
        for manager in self.managers:
            setattr(self, manager.name, manager(self))

    def fetch_data(self, method: str, endpoint: str, params: dict[str, typing.Any]) -> dict[str, typing.Any]:

        if params.get("api_key") is None:
            params.update({"key": self.api_key})

        url = urljoin(self.BASE_URL, endpoint)

        response = self.session.request(method, url, params=params)
        response.raise_for_status()
        response_json = response.json()
        raise_for_errors(response_json, {"101"}, CrendetialError)
        return response_json
