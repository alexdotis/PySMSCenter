import types
from collections.abc import Mapping
from typing import Any, ClassVar, Self, cast
from urllib.parse import urljoin

from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from pysmscenter.managers.balance_manager import BalanceManager
from pysmscenter.managers.contact_manager import ContactManager
from pysmscenter.managers.group_manager import GroupManager
from pysmscenter.managers.history_manager import HistoryManager
from pysmscenter.managers.hlr_manager import HLRManager
from pysmscenter.managers.manager import Manager
from pysmscenter.managers.mobile_manager import MobileManager
from pysmscenter.managers.purchase_manager import PurchaseManager
from pysmscenter.managers.sms_manager import SmsManager
from pysmscenter.managers.status_manager import StatusManager
from pysmscenter.managers.two_factor_manager import TwoFactorManager
from pysmscenter.managers.user_manager import UserManager
from pysmscenter.types.key_types import KeyRawResponse

from .exceptions import CredentialError

type Timeout = tuple[float, float]


class BaseHTTPClient:
    BASE_URL: str = "https://smscenter.gr/api/"
    DEFAULT_TYPE: str = "json"
    DEFAULT_TIMEOUT: ClassVar[Timeout] = (5.0, 30.0)

    def __init__(
        self, max_retries: int = 0, timeout: Timeout | None = DEFAULT_TIMEOUT, backoff_factor: float = 0.5
    ) -> None:
        self.max_retries = max_retries
        self.timeout = timeout
        self.backoff_factor = backoff_factor
        self._session: Session = self._build_session()
        self._closed: bool = False

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} base_url={self.BASE_URL!r}>"

    @property
    def session(self) -> Session:
        if self._closed:
            raise RuntimeError("Session is closed")
        return self._session

    def close(self) -> None:
        if not self._closed:
            self._session.close()
            self._closed = True

    def __enter__(self) -> Self:
        if self._closed:
            raise RuntimeError("Cannot enter context with closed session")
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: types.TracebackType | None,
    ) -> bool:
        self.close()
        return False

    def _build_session(self) -> Session:
        session = Session()

        retry_strategy = Retry(
            total=self.max_retries,
            backoff_factor=self.backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=None,
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def _build_params(self, params: Mapping[str, Any] | None = None) -> dict[str, Any]:
        params_dict = dict(params) if params is not None else {}
        params_dict.setdefault("type", self.DEFAULT_TYPE)
        return params_dict

    def _request(self, method: str, endpoint: str, params: Mapping[str, Any] | None = None) -> dict[str, Any]:
        url = urljoin(self.BASE_URL, endpoint)
        request_params = self._build_params(params)
        method = method.upper()
        response = self.session.request(method, url, params=request_params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()


class SMSAuthClient(BaseHTTPClient):
    def get_key(self, username: str, password: str) -> KeyRawResponse:
        """
        Get an API key for the given username and password.

        Args:
            username (str): The username to authenticate with.
            password (str): The password to authenticate with.
        Returns:
            KeyRawResponse: The API key for the authenticated user.
        """
        response = self._request("GET", "key/get", params={"username": username, "password": password})
        return cast(KeyRawResponse, response)

    def reset_key(self, username: str, password: str) -> KeyRawResponse:
        """
        Reset the API key for the authenticated user.

        Returns:
            KeyRawResponse: The new API key for the authenticated user.
        """

        response = self._request("GET", "key/reset", params={"username": username, "password": password})
        return cast(KeyRawResponse, response)


class SMSClient(BaseHTTPClient):
    mobile: "MobileManager"
    sms: "SmsManager"
    balance: "BalanceManager"
    history: "HistoryManager"
    status: "StatusManager"
    contact: "ContactManager"
    group: "GroupManager"
    purchase: "PurchaseManager"
    hlr: "HLRManager"
    two_factor: "TwoFactorManager"
    user: "UserManager"

    managers: ClassVar[list[type[Manager]]] = [
        MobileManager,
        SmsManager,
        BalanceManager,
        HistoryManager,
        StatusManager,
        ContactManager,
        GroupManager,
        PurchaseManager,
        HLRManager,
        TwoFactorManager,
        UserManager,
    ]

    def __init__(
        self, api_key: str, max_retries: int = 0, timeout: Timeout | None = BaseHTTPClient.DEFAULT_TIMEOUT
    ) -> None:
        super().__init__(max_retries=max_retries, timeout=timeout)
        self.api_key = api_key
        if not api_key:
            raise CredentialError("API key is required")

        self._setup_managers()

    @classmethod
    def from_credentials(
        cls,
        username: str,
        password: str,
        max_retries: int = 0,
        timeout: Timeout | None = BaseHTTPClient.DEFAULT_TIMEOUT,
    ) -> "SMSClient":
        """
        Create an SMSClient instance from a username and password.

        Args:
            username (str): The username to authenticate with.
            password (str): The password to authenticate with.
            max_retries (int, optional): The maximum number of retries for HTTP requests. Defaults to 0.
            timeout (Timeout, optional): The timeout for HTTP requests. Defaults to BaseHTTPClient.DEFAULT_TIMEOUT.
        Returns:
            SMSClient: An instance of SMSClient authenticated with the provided credentials.
        """
        auth_client = SMSAuthClient(max_retries=max_retries, timeout=timeout)
        try:
            key_response = auth_client.get_key(username, password)
        finally:
            auth_client.close()

        api_key = key_response.get("key")
        if not api_key:
            raise CredentialError("Failed to retrieve API key with provided credentials")
        return cls(api_key=api_key, max_retries=max_retries, timeout=timeout)

    @classmethod
    def reset_api_key(
        cls,
        username: str,
        password: str,
        max_retries: int = 0,
        timeout: Timeout | None = BaseHTTPClient.DEFAULT_TIMEOUT,
    ) -> str:
        auth_client = SMSAuthClient(max_retries=max_retries, timeout=timeout)
        try:
            key_response = auth_client.reset_key(username, password)
        finally:
            auth_client.close()

        new_api_key = key_response.get("key")
        if not new_api_key:
            raise CredentialError("Failed to reset API key with provided credentials")

        return new_api_key

    def _setup_managers(self) -> None:
        for manager in self.managers:
            setattr(self, manager.name, manager(self))

    def fetch_data(
        self,
        method: str,
        endpoint: str,
        params: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        response_json = self._request(method, endpoint, params=params)
        self._raise_for_credential_error(response_json)
        return response_json

    def _build_params(self, params: Mapping[str, Any] | None = None) -> dict[str, Any]:
        params_dict = super()._build_params(params)
        params_dict.update({"key": self.api_key})
        return params_dict

    @staticmethod
    def _raise_for_credential_error(response_json: Mapping[str, Any]) -> None:
        if str(response_json.get("status")) == "0" and str(response_json.get("error")) == "101":
            raise CredentialError(
                response_json.get("remarks"),
                code=str(response_json.get("error")),
                response=dict(response_json),
            )
