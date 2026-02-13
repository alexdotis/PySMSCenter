from typing import Any

import pytest

from pysmscenter import SMSClient
from pysmscenter.exceptions import SMSClientError, UserCommentExceptionError, UserExceptionError


class TestUserManager:
    def test_add_user(self, client: SMSClient, mocker: Any) -> None:
        fake_response = {
            "status": "1",
            "error": "0",
            "remarks": "User added successfully",
            "user": {"userId": "12345", "email": "fake@hotmail.com"},
        }

        call_mock = mocker.patch.object(client.user, "call", return_value=fake_response)

        response = client.user.add(email="fake@hotmail.com", password="fakepassword")  # noqa: S106

        call_mock.assert_called_once_with(
            "GET",
            "user/add",
            params={"email": "fake@hotmail.com", "password": "fakepassword"},
        )
        assert response == fake_response

    def test_add_user_invalid_email(self, client: SMSClient) -> None:
        with pytest.raises(ValueError, match="Invalid email address: invalid-email") as exc_info:
            client.user.add(email="invalid-email", password="fakepassword")  # noqa: S106

        assert str(exc_info.value) == "Invalid email address: invalid-email"

    @pytest.mark.parametrize(
        ("error_core", "error_message"),
        [
            ("601", "Error: User already exists"),
            ("602", "Error: You have reached the maximum number of sub-accounts allowed"),
        ],
    )
    def test_add_user_api_error(self, client: SMSClient, mocker: Any, error_core: str, error_message: str) -> None:
        fake_response = {
            "status": "0",
            "error": error_core,
            "remarks": error_message,
        }

        mocker.patch.object(client.user, "call", return_value=fake_response)
        with pytest.raises(UserExceptionError) as exc_info:
            client.user.add(email="fake@hotmail.com", password="fakepassword")  # noqa: S106
        assert exc_info.value.code == error_core
        assert exc_info.value.args[0]

    def test_list_users(self, client: SMSClient, mocker: Any) -> None:
        fake_response = {
            "0": {
                "userId": "123",
                "username": "RSL.123",
                "email": "fakemail@hotmail.com",
                "balance": "0",
                "mobile": "306912300000",
                "key": None,
            },
            "1": {
                "userId": "124",
                "username": "RSL.124",
                "email": "fakemail1@gmail.com",
                "balance": "0",
                "mobile": "306912400000",
                "key": None,
            },
            "status": "1",
            "total": "2",
            "remarks": "Success",
            "error": "0",
        }
        call_mock = mocker.patch.object(client.user, "call", return_value=fake_response)
        response = client.user.list()
        call_mock.assert_called_once_with("GET", "user/list")
        assert response == fake_response

    def test_topup_user(self, client: SMSClient, mocker: Any) -> None:
        fake_response = {
            "status": "1",
            "error": "0",
            "remarks": "Success",
            "user": {"userId": "12345", "balance": 100},
        }

        call_mock = mocker.patch.object(client.user, "call", return_value=fake_response)

        response = client.user.topup(user_id="12345", sms="10", cost="5")

        call_mock.assert_called_once_with(
            "GET",
            "user/topup",
            params={"userId": "12345", "sms": "10", "cost": "5"},
        )
        assert response == fake_response

    @pytest.mark.parametrize(
        ("error_core", "error_message"),
        [
            ("206", "Error: Parameter [sms] is invalid"),
            ("207", "Error: Parameter [cost] is invalid"),
            ("208", "Error: Parameter [userId] is invalid"),
            ("209", "Error: User not found"),
            ("210", "Error: There is not enough balance in the main account to top up the sub-account"),
            ("211", "Error: Insufficient balance in main account"),
        ],
    )
    def test_topup_user_api_error(self, client: SMSClient, mocker: Any, error_core: str, error_message: str) -> None:
        fake_response = {
            "status": "0",
            "error": error_core,
            "remarks": error_message,
        }

        mocker.patch.object(client.user, "call", return_value=fake_response)
        with pytest.raises(UserExceptionError) as exc_info:
            client.user.topup(user_id="12345", sms="10", cost="5")
        assert exc_info.value.code == error_core
        assert exc_info.value.args[0] == error_message

    def test_add_comment(self, client: SMSClient, mocker: Any) -> None:
        fake_response = {
            "status": "1",
            "error": "0",
            "remarks": "Success",
            "comment": {"commentId": "12345"},
        }

        call_mock = mocker.patch.object(client.user, "call", return_value=fake_response)

        response = client.user.add_comment(user_id="12345", comment="This is a test comment")

        call_mock.assert_called_once_with(
            "GET",
            "user/comment/add",
            params={"userId": "12345", "comment": "This is a test comment"},
        )
        assert response == fake_response

    @pytest.mark.parametrize(
        ("error_core", "error_message"),
        [
            ("208", "Error: Parameter [userId] is empty"),
            ("213", "Error: User not found"),
            ("212", "Error: Parameter [comment] is empty"),
        ],
    )
    def test_add_comment_api_error(self, client: SMSClient, mocker: Any, error_core: str, error_message: str) -> None:
        fake_response = {
            "status": "0",
            "error": error_core,
            "remarks": error_message,
        }

        mocker.patch.object(client.user, "call", return_value=fake_response)
        with pytest.raises(UserCommentExceptionError) as exc_info:
            client.user.add_comment(user_id="12345", comment="This is a test comment")
        assert exc_info.value.code == error_core
        assert exc_info.value.args[0]

    def test_delete_comment(self, client: SMSClient, mocker: Any) -> None:
        fake_response = {
            "status": "1",
            "error": "0",
            "remarks": "Success",
        }

        call_mock = mocker.patch.object(client.user, "call", return_value=fake_response)
        response = client.user.delete_comment(comment_id="12345")
        call_mock.assert_called_once_with(
            "GET",
            "user/comment/delete",
            params={"commentId": "12345"},
        )
        assert response == fake_response

    @pytest.mark.parametrize(
        ("error_core", "error_message"),
        [
            ("212", "Error: Parameter [comment] not found"),
            ("220", "Error: Parameter [commentId] not found"),
        ],
    )
    def test_delete_comment_api_error(
        self, client: SMSClient, mocker: Any, error_core: str, error_message: str
    ) -> None:
        fake_response = {
            "status": "0",
            "error": error_core,
            "remarks": error_message,
        }

        mocker.patch.object(client.user, "call", return_value=fake_response)
        with pytest.raises(SMSClientError) as exc_info:
            client.user.delete_comment(comment_id="12345")
        assert exc_info.value.code == error_core
        assert exc_info.value.args[0]

    def test_list_comments(self, client: SMSClient, mocker: Any) -> None:
        fake_response = {
            "status": "1",
            "error": "0",
            "remarks": "Success",
            "total": "2",
            "comments": [
                {"commentId": "12345", "comment": "This is a test comment"},
                {"commentId": "12346", "comment": "This is another test comment"},
            ],
        }

        call_mock = mocker.patch.object(client.user, "call", return_value=fake_response)
        response = client.user.comments(user_id="12345")
        call_mock.assert_called_once_with(
            "GET",
            "user/comment/list",
            params={"userId": "12345"},
        )
        assert response == fake_response

    @pytest.mark.parametrize(
        ("error_core", "error_message"),
        [
            ("208", "Error: Parameter [userId] is empty"),
            ("209", "Error: User not found"),
        ],
    )
    def test_list_comments_api_error(
        self, client: SMSClient, mocker: Any, error_core: str, error_message: str
    ) -> None:
        fake_response = {
            "status": "0",
            "error": error_core,
            "remarks": error_message,
        }

        mocker.patch.object(client.user, "call", return_value=fake_response)
        with pytest.raises(SMSClientError) as exc_info:
            client.user.comments(user_id="12345")
        assert exc_info.value.code == error_core
        assert exc_info.value.args[0]
