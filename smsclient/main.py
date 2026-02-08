import types
from collections.abc import Mapping
from typing import Any, ClassVar
from urllib.parse import urljoin

from requests import Session
from requests.adapters import HTTPAdapter

from smsclient.managers.balance_manager import BalanceManager
from smsclient.managers.contact_manager import ContactManager
from smsclient.managers.group_manager import GroupManager
from smsclient.managers.history_manager import HistoryManager
from smsclient.managers.manager import Manager
from smsclient.managers.mobile_manager import MobileManager
from smsclient.managers.purchase_manager import PurchaseManager
from smsclient.managers.sms_manager import SmsManager
from smsclient.managers.status_manager import StatusManager

from .exceptions import CredentialError


class SMSClient:
    BASE_URL: str = "https://smscenter.gr/api/"
    DEFAULT_TYPE: str = "json"

    mobile: "MobileManager"
    sms: "SmsManager"
    balance: "BalanceManager"
    history: "HistoryManager"
    status: "StatusManager"
    contact: "ContactManager"
    group: "GroupManager"
    purchase: "PurchaseManager"

    managers: ClassVar[list[type[Manager]]] = [
        MobileManager,
        SmsManager,
        BalanceManager,
        HistoryManager,
        StatusManager,
        ContactManager,
        GroupManager,
        PurchaseManager,
    ]

    def __init__(self, api_key: str, max_retries: int = 0) -> None:
        self.api_key = api_key
        if not api_key:
            raise CredentialError("API key is required")
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

    def fetch_data(
        self,
        method: str,
        endpoint: str,
        params: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        params_dict = dict(params) if params is not None else {}
        params_dict.setdefault("type", self.DEFAULT_TYPE)
        params_dict.update({"key": self.api_key})

        url = urljoin(self.BASE_URL, endpoint)

        response = self.session.request(method, url, params=params_dict)
        response.raise_for_status()
        response_json = response.json()

        if str(response_json.get("status")) == "0" and str(response_json.get("error")) == "101":
            raise CredentialError(
                response_json.get("remarks"),
                code=str(response_json.get("error")),
                response=response_json,
            )
        return response_json
