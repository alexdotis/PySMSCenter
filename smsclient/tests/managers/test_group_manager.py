import re
from typing import Any

import pytest

from smsclient import SMSClient
from smsclient.exceptions import GroupExceptionError


class TestGroupManager:
    def test_create_group(self, client: SMSClient, mocker: Any) -> None:
        fake_response = {"status": "1", "remarks": "Success", "error": "0", "groupId": "12345"}

        call_mock = mocker.patch.object(
            client.group,
            "call",
            return_value=fake_response,
        )

        response = client.group.add(name="Test Group")

        call_mock.assert_called_once_with(
            "GET",
            "group/add",
            {
                "name": "Test Group",
            },
        )
        assert response == fake_response

    def test_create_group_raises_exception_on_error(self, client: SMSClient, mocker: Any) -> None:
        error_code = "213"
        error_response = "Error: No name parameter"

        fake_response = {"status": "0", "remarks": error_response, "error": error_code}
        mocker.patch.object(
            client.group,
            "call",
            return_value=fake_response,
        )
        with pytest.raises(GroupExceptionError, match=error_response) as exc:
            client.group.add(name="")
        assert exc.value.code == error_code
        assert exc.value.args[0]

    def test_delete_group(self, client: SMSClient, mocker: Any) -> None:
        fake_response = {"status": "1", "remarks": "Success", "error": "0"}

        call_mock = mocker.patch.object(
            client.group,
            "call",
            return_value=fake_response,
        )

        response = client.group.delete(group_id="12345")

        call_mock.assert_called_once_with(
            "GET",
            "group/delete",
            {
                "groupId": "12345",
            },
        )
        assert response == fake_response

    @pytest.mark.parametrize(
        ("error_code", "error_response"),
        [("215", "Error: No [groupId] parameter"), ("217", "Error: [groupId:123456] not found")],
    )
    def test_delete_group_raises_exception_on_error(
        self,
        client: SMSClient,
        mocker: Any,
        error_code: str,
        error_response: str,
    ) -> None:
        fake_response = {"status": "0", "remarks": error_response, "error": error_code}
        mocker.patch.object(
            client.group,
            "call",
            return_value=fake_response,
        )
        with pytest.raises(GroupExceptionError, match=re.escape(error_response)) as exc:
            client.group.delete(group_id="invalid")
        assert exc.value.code == error_code
        assert exc.value.args[0]

    def test_list_groups(self, client: SMSClient, mocker: Any) -> None:
        fake_response = {
            "status": "1",
            "remarks": "Success",
            "error": "0",
            "total": "2",
            "groups": [{"groupId": "123", "name": "New Group"}, {"groupId": "124", "name": "New Group 1"}],
        }

        call_mock = mocker.patch.object(
            client.group,
            "call",
            return_value=fake_response,
        )

        response = client.group.list()

        call_mock.assert_called_once_with(
            "GET",
            "group/list",
        )
        assert response == fake_response

    def test_list_groups_empty(self, client: SMSClient, mocker: Any) -> None:
        fake_response = {"status": "1", "remarks": "Success", "error": "0", "total": "0"}

        call_mock = mocker.patch.object(
            client.group,
            "call",
            return_value=fake_response,
        )

        response = client.group.list()

        call_mock.assert_called_once_with(
            "GET",
            "group/list",
        )
        assert response == fake_response

    def test_add_contact_to_group(self, client: SMSClient, mocker: Any) -> None:
        fake_response = {
            "status": "1",
            "remarks": "Success",
            "error": "0",
            "group": {"contact": {"contactGroupId": "67890"}},
        }

        call_mock = mocker.patch.object(
            client.group,
            "call",
            return_value=fake_response,
        )

        response = client.group.add_contact(group_id="12345", contact_id="67890")

        call_mock.assert_called_once_with(
            "GET",
            "group/addContact",
            {
                "groupId": "12345",
                "contactId": "67890",
            },
        )
        assert response == fake_response

    @pytest.mark.parametrize(
        ("error_code", "error_response"),
        [
            ("215", "Error: No [groupId] parameter"),
            ("217", "Error: [groupId:123456] not found"),
        ],
    )
    def test_add_contact_to_group_raises_exception_on_error(
        self,
        client: SMSClient,
        mocker: Any,
        error_code: str,
        error_response: str,
    ) -> None:
        fake_response = {"status": "0", "remarks": error_response, "error": error_code}
        mocker.patch.object(
            client.group,
            "call",
            return_value=fake_response,
        )
        with pytest.raises(GroupExceptionError, match=re.escape(error_response)) as exc:
            client.group.add_contact(group_id="invalid", contact_id="invalid")
        assert exc.value.code == error_code
        assert exc.value.args[0]

    def test_delete_contact_from_group_success(self, client: SMSClient, mocker: Any) -> None:
        fake_response = {"status": "1", "remarks": "Success", "error": "0"}

        call_mock = mocker.patch.object(
            client.group,
            "call",
            return_value=fake_response,
        )
        response = client.group.delete_contact(group_id="12345", contact_id="67890")
        call_mock.assert_called_once_with(
            "GET",
            "group/deleteContact",
            {
                "groupId": "12345",
                "contactId": "67890",
            },
        )
        assert response == fake_response

    def test_delete_contact_from_group_with_contact_group_id(self, client: SMSClient, mocker: Any) -> None:
        fake_response = {"status": "1", "remarks": "Success", "error": "0"}

        call_mock = mocker.patch.object(
            client.group,
            "call",
            return_value=fake_response,
        )
        response = client.group.delete_contact(contact_group_id="67890")
        call_mock.assert_called_once_with(
            "GET",
            "group/deleteContact",
            {
                "contactGroupId": "67890",
            },
        )
        assert response == fake_response

    @pytest.mark.parametrize(
        ("error_code", "error_response"),
        [
            ("215", "Error: No [groupId] parameter"),
            ("217", "Error: [groupId:123456] not found"),
        ],
    )
    def test_delete_contact_from_group_raises_exception_on_error(
        self,
        client: SMSClient,
        mocker: Any,
        error_code: str,
        error_response: str,
    ) -> None:
        fake_response = {"status": "0", "remarks": error_response, "error": error_code}
        mocker.patch.object(
            client.group,
            "call",
            return_value=fake_response,
        )
        with pytest.raises(GroupExceptionError, match=re.escape(error_response)) as exc:
            client.group.delete_contact(group_id="invalid", contact_id="invalid")
        assert exc.value.code == error_code
        assert exc.value.args[0]

    @pytest.mark.parametrize(
        ("error_code", "error_response"),
        [
            ("215", "Error: No [groupId] parameter"),
            ("217", "Error: [groupId:123456] not found"),
        ],
    )
    def test_delete_contact_from_group_contact_id_raises_exception_on_error(
        self,
        client: SMSClient,
        mocker: Any,
        error_code: str,
        error_response: str,
    ) -> None:
        fake_response = {"status": "0", "remarks": error_response, "error": error_code}
        mocker.patch.object(
            client.group,
            "call",
            return_value=fake_response,
        )
        with pytest.raises(GroupExceptionError, match=re.escape(error_response)) as exc:
            client.group.delete_contact(contact_group_id="invalid")
        assert exc.value.code == error_code
        assert exc.value.args[0]

    @pytest.mark.parametrize(
        "params",
        [
            {},
            {"group_id": "123"},
            {"contact_id": "456"},
            {"group_id": "123", "contact_group_id": "789"},
            {"contact_id": "456", "contact_group_id": "789"},
        ],
    )
    def test_delete_contact_invalid_arguments_raise_value_error(
        self,
        client: SMSClient,
        params: dict[str, str],
    ) -> None:
        with pytest.raises(
            ValueError, match="Either contact_group_id or both group_id and contact_id must be provided"
        ):
            client.group.delete_contact(**params)

    def test_delete_group_all_contacts_success(self, client: SMSClient, mocker: Any) -> None:
        fake_response = {"status": "1", "remarks": "Success", "error": "0"}

        call_mock = mocker.patch.object(
            client.group,
            "call",
            return_value=fake_response,
        )
        response = client.group.delete_all_contacts(group_id="12345")
        call_mock.assert_called_once_with(
            "GET",
            "group/deleteAllContacts",
            {
                "groupId": "12345",
            },
        )
        assert response == fake_response

    @pytest.mark.parametrize(
        ("error_code", "error_response"),
        [
            ("215", "Error: No [groupId] parameter"),
            ("217", "Error: [groupId:123456] not found"),
        ],
    )
    def test_delete_group_all_contacts_raises_exception_on_error(
        self,
        client: SMSClient,
        mocker: Any,
        error_code: str,
        error_response: str,
    ) -> None:
        fake_response = {"status": "0", "remarks": error_response, "error": error_code}
        mocker.patch.object(
            client.group,
            "call",
            return_value=fake_response,
        )
        with pytest.raises(GroupExceptionError, match=re.escape(error_response)) as exc:
            client.group.delete_all_contacts(group_id="invalid")
        assert exc.value.code == error_code
        assert exc.value.args[0]
