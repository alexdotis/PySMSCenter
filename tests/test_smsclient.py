from typing import Any
from urllib.parse import urljoin

import pytest

from smsclient import SMSClient
from smsclient.exceptions import CredentialError


class TestSMSClient:
    def test_init_requires_api_key(self) -> None:
        with pytest.raises(CredentialError, match="API key is required"):
            SMSClient("")

    def test_repr(self, client: SMSClient) -> None:
        assert repr(client) == f"<SMSClient base_url={SMSClient.BASE_URL!r}>"

    def test_session_creates_and_reuses_session(self, mocker: Any) -> None:
        mock_session = mocker.Mock()
        session_ctor = mocker.patch("smsclient.main.Session", return_value=mock_session)
        adapter = mocker.Mock()
        adapter_ctor = mocker.patch("smsclient.main.HTTPAdapter", return_value=adapter)

        client = SMSClient("test-api-key", max_retries=2)

        session_one = client.session
        session_two = client.session

        assert session_one is mock_session
        assert session_two is mock_session
        session_ctor.assert_called_once_with()
        adapter_ctor.assert_called_once_with(max_retries=2)
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
        assert client._session is None
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
        assert client._session is None
        assert client._closed is True

    def test_setup_managers(self, client: SMSClient) -> None:
        for manager_cls in SMSClient.managers:
            manager = getattr(client, manager_cls.name)
            assert isinstance(manager, manager_cls)
            assert manager.client is client

    def test_fetch_data_sets_defaults_and_calls_request(self, client: SMSClient, mocker: Any) -> None:
        response_json = {"status": "1", "error": "0"}
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
        response_json = {"status": "1", "error": "0"}
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
