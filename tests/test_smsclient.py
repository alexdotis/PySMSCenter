from typing import Any
from urllib.parse import urljoin

import pytest
from urllib3.util.retry import Retry

from pysmscenter import SMSClient
from pysmscenter.exceptions import CredentialError
from pysmscenter.main import BaseHTTPClient, SMSAuthClient


@pytest.fixture
def auth_client_fixture(mocker: Any) -> tuple[Any, Any]:
    auth_client = mocker.Mock()
    auth_ctor = mocker.patch("pysmscenter.main.SMSAuthClient", return_value=auth_client)
    return auth_client, auth_ctor


class TestSMSClient:
    def test_init_requires_api_key(self) -> None:
        with pytest.raises(CredentialError, match="API key is required"):
            SMSClient("")

    def test_repr(self, client: SMSClient) -> None:
        assert repr(client) == f"<SMSClient base_url={SMSClient.BASE_URL!r}>"

    def test_session_creates_and_reuses_session(self, mocker: Any) -> None:
        mock_session = mocker.Mock()
        session_ctor = mocker.patch("pysmscenter.main.Session", return_value=mock_session)
        adapter = mocker.Mock()
        adapter_ctor = mocker.patch("pysmscenter.main.HTTPAdapter", return_value=adapter)

        client = SMSClient("test-api-key", max_retries=2)

        session_one = client.session
        session_two = client.session

        assert session_one is mock_session
        assert session_two is mock_session
        session_ctor.assert_called_once_with()
        adapter_ctor.assert_called_once()
        retry_arg = adapter_ctor.call_args.kwargs.get("max_retries")
        assert isinstance(retry_arg, Retry)
        mock_session.mount.assert_any_call("http://", adapter)
        mock_session.mount.assert_any_call("https://", adapter)
        assert mock_session.mount.call_count == 2

    def test_session_raises_when_closed(self, client: SMSClient) -> None:
        client.close()

        with pytest.raises(RuntimeError, match="Session is closed"):
            _ = client.session

    def test_close_closes_session(self, client: SMSClient, mocker: Any) -> None:
        mock_session = mocker.Mock()
        client._session = mock_session

        client.close()

        mock_session.close.assert_called_once_with()
        assert client._session is mock_session
        assert client._closed is True

    def test_context_manager_closes_session(self, mocker: Any) -> None:
        client = SMSClient("test-api-key")
        mock_session = mocker.Mock()
        client._session = mock_session

        result = client.__enter__()
        assert result is client

        exit_result = client.__exit__(None, None, None)
        assert exit_result is False
        mock_session.close.assert_called_once_with()
        assert client._session is mock_session
        assert client._closed is True

    def test_setup_managers(self, client: SMSClient) -> None:
        for manager_cls in SMSClient.managers:
            manager = getattr(client, manager_cls.name)
            assert isinstance(manager, manager_cls)
            assert manager.client is client

    def test_fetch_data_sets_defaults_and_calls_request(self, client: SMSClient, mocker: Any) -> None:
        response_json = {
            "status": "1",
            "balance": "2",
            "remarks": "Success",
            "error": "0",
        }
        response = mocker.Mock()
        response.json.return_value = response_json
        mock_session = mocker.Mock()
        mock_session.request.return_value = response
        client._session = mock_session

        result = client.fetch_data("GET", "balance")

        mock_session.request.assert_called_once_with(
            "GET",
            urljoin(SMSClient.BASE_URL, "balance"),
            params={
                "type": SMSClient.DEFAULT_TYPE,
                "key": "test-api-key",
            },
            timeout=client.timeout,
        )
        response.raise_for_status.assert_called_once_with()
        assert result == response_json

    def test_fetch_data_overrides_key_and_preserves_type(self, client: SMSClient, mocker: Any) -> None:
        response_json = {
            "status": "1",
            "balance": "2",
            "remarks": "Success",
            "error": "0",
        }
        response = mocker.Mock()
        response.json.return_value = response_json
        mock_session = mocker.Mock()
        mock_session.request.return_value = response
        client._session = mock_session

        result = client.fetch_data(
            "GET",
            "mobile/check",
            params={"type": "xml", "foo": "bar", "key": "override"},
        )

        mock_session.request.assert_called_once_with(
            "GET",
            urljoin(SMSClient.BASE_URL, "mobile/check"),
            params={
                "type": "xml",
                "foo": "bar",
                "key": "test-api-key",
            },
            timeout=client.timeout,
        )
        response.raise_for_status.assert_called_once_with()
        assert result == response_json

    def test_fetch_data_raises_credential_error(self, client: SMSClient, mocker: Any) -> None:
        response_json = {"status": 0, "error": 101, "remarks": "Invalid API key"}
        response = mocker.Mock()
        response.json.return_value = response_json
        mock_session = mocker.Mock()
        mock_session.request.return_value = response
        client._session = mock_session

        with pytest.raises(CredentialError, match="Invalid API key") as exc:
            client.fetch_data("GET", "balance")

        assert exc.value.code == "101"
        assert exc.value.message == "Invalid API key"
        assert exc.value.response == response_json

    def test_from_credentials_uses_auth_client(self, auth_client_fixture: tuple[Any, Any]) -> None:
        auth_client, auth_ctor = auth_client_fixture
        auth_client.get_key.return_value = {
            "status": "1",
            "remarks": "Success",
            "key": "fake_api_key_123456",
            "error": "0",
        }

        client = SMSClient.from_credentials("user", "pass", max_retries=2)

        kwargs = auth_ctor.call_args.kwargs
        assert kwargs["max_retries"] == 2
        assert kwargs["timeout"] == SMSClient.DEFAULT_TIMEOUT
        auth_client.get_key.assert_called_once_with("user", "pass")
        auth_client.close.assert_called_once_with()
        assert client.api_key == "fake_api_key_123456"

    def test_from_credentials_raises_when_missing_key(self, auth_client_fixture: tuple[Any, Any]) -> None:
        auth_client, auth_ctor = auth_client_fixture
        auth_client.get_key.return_value = {
            "status": "1",
            "balance": "2",
            "remarks": "Error: Check your credentials",
            "error": "101",
        }

        with pytest.raises(CredentialError, match="Failed to retrieve API key"):
            SMSClient.from_credentials("user", "pass")

        auth_ctor.assert_called_once_with(max_retries=0, timeout=SMSClient.DEFAULT_TIMEOUT)
        auth_client.close.assert_called_once_with()

    def test_reset_api_key_returns_new_key(self, auth_client_fixture: tuple[Any, Any]) -> None:
        auth_client, auth_ctor = auth_client_fixture
        auth_client.reset_key.return_value = {
            "status": "1",
            "remarks": "Success",
            "key": "new_fake_api_key_654321",
            "error": "0",
        }

        result = SMSClient.reset_api_key("user", "pass", max_retries=3)

        auth_ctor.assert_called_once_with(max_retries=3, timeout=SMSClient.DEFAULT_TIMEOUT)
        auth_client.reset_key.assert_called_once_with("user", "pass")
        auth_client.close.assert_called_once_with()
        assert result == "new_fake_api_key_654321"

    def test_reset_api_key_raises_when_missing_key(self, auth_client_fixture: tuple[Any, Any]) -> None:
        auth_client, auth_ctor = auth_client_fixture
        auth_client.reset_key.return_value = {
            "status": "1",
            "balance": "2",
            "remarks": "Error: Check your credentials",
            "error": "101",
        }

        with pytest.raises(CredentialError, match="Failed to reset API key"):
            SMSClient.reset_api_key("user", "pass")

        auth_ctor.assert_called_once_with(max_retries=0, timeout=SMSClient.DEFAULT_TIMEOUT)
        auth_client.close.assert_called_once_with()


class TestBaseHTTPClient:
    def test_repr(self) -> None:
        client = BaseHTTPClient()
        assert repr(client) == f"<BaseHTTPClient base_url={BaseHTTPClient.BASE_URL!r}>"

    def test_build_params_defaults_type(self) -> None:
        client = BaseHTTPClient()

        result = client._build_params({"foo": "bar"})

        assert result == {"foo": "bar", "type": BaseHTTPClient.DEFAULT_TYPE}

    def test_request_uses_base_url_and_timeout(self, mocker: Any) -> None:
        client = BaseHTTPClient(timeout=(1.0, 2.0))
        mock_session = mocker.Mock()
        client._session = mock_session
        response = mocker.Mock()
        response.json.return_value = {
            "status": "1",
            "balance": "2",
            "remarks": "Success",
            "error": "0",
        }
        mock_session.request.return_value = response

        result = client._request("GET", "health", params={"foo": "bar"})

        mock_session.request.assert_called_once_with(
            "GET",
            urljoin(BaseHTTPClient.BASE_URL, "health"),
            params={"foo": "bar", "type": BaseHTTPClient.DEFAULT_TYPE},
            timeout=client.timeout,
        )
        response.raise_for_status.assert_called_once_with()
        assert result == {
            "status": "1",
            "balance": "2",
            "remarks": "Success",
            "error": "0",
        }


class TestSMSAuthClient:
    def test_get_key(self, mocker: Any) -> None:
        client = SMSAuthClient()
        request_mock = mocker.patch.object(
            client,
            "_request",
            return_value={
                "status": "1",
                "remarks": "Success",
                "key": "fake_api_key_123456",
                "error": "0",
            },
        )

        result = client.get_key("user", "pass")

        request_mock.assert_called_once_with("GET", "key/get", params={"username": "user", "password": "pass"})
        assert result == {
            "status": "1",
            "remarks": "Success",
            "key": "fake_api_key_123456",
            "error": "0",
        }

    def test_reset_key(self, mocker: Any) -> None:
        client = SMSAuthClient()
        request_mock = mocker.patch.object(
            client,
            "_request",
            return_value={
                "status": "1",
                "remarks": "Success",
                "key": "new_fake_api_key_654321",
                "error": "0",
            },
        )

        result = client.reset_key("user", "pass")

        request_mock.assert_called_once_with("GET", "key/reset", params={"username": "user", "password": "pass"})
        assert result == {
            "status": "1",
            "remarks": "Success",
            "key": "new_fake_api_key_654321",
            "error": "0",
        }
