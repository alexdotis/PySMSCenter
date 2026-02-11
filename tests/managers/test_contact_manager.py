import re
from datetime import date
from typing import Any

import pytest

from smsclient import SMSClient
from smsclient.exceptions import ContactExceptionError


class TestContactManager:
    def test_contact_add_calls_api(self, client: SMSClient, mocker: Any) -> None:
        fake_response = {
            "status": "1",
            "remarks": "Success",
            "error": "0",
            "contact": {"contactId": "123"},
        }

        call_mock = mocker.patch.object(
            client.contact,
            "call",
            return_value=fake_response,
        )

        response = client.contact.add(
            mobile="6912345678",
            name="John",
            surname="Doe",
            birthday=date(1990, 1, 5),
        )

        call_mock.assert_called_once_with(
            "GET",
            "contact/add",
            {
                "mobile": "6912345678",
                "name": "John",
                "surname": "Doe",
                "full_name": "",
                "vname": "",
                "vusername": "",
                "birthday": "1990-01-05",
                "nameday": None,
            },
        )

        assert response == fake_response

    @pytest.mark.parametrize(
        ("field", "value"),
        [
            ("nameday", "1990/01/05"),
            ("nameday", "05-01-1990"),
            ("nameday", "January 5, 1990"),
            ("nameday", "19900105"),
            ("birthday", "1990/01/05"),
            ("birthday", "05-01-1990"),
            ("birthday", "January 5, 1990"),
            ("birthday", "19900105"),
        ],
    )
    def test_contact_add_invalid_date_format_raises(self, client: SMSClient, field: str, value: str) -> None:
        with pytest.raises(ContactExceptionError, match="Invalid date format"):
            client.contact.add(
                mobile="306912345678",
                **{field: value},
            )

    @pytest.mark.parametrize(
        ("error_code", "error_message"),
        [
            ("201", "Error: Parameter [mobile] cannot be parsed"),
            ("202", "Error: Contact already exists with this mobile"),
            ("203", "Error: Mobile number is Opt-out"),
            ("205", "Error: No [mobile] parameter"),
            ("204", "Error: Contact couldnt be added"),
        ],
    )
    def test_contact_add_raises_on_error(
        self,
        client: SMSClient,
        mocker: Any,
        error_code: str,
        error_message: str,
    ) -> None:
        fake_response = {
            "status": "0",
            "error": error_code,
            "remarks": error_message,
        }

        mocker.patch.object(
            client.contact,
            "call",
            return_value=fake_response,
        )

        with pytest.raises(ContactExceptionError, match=re.escape(error_message)) as exc:
            client.contact.add(mobile="invalid")

        assert exc.value.code == error_code
        assert exc.value.args[0]

    def test_contact_list_calls_api(self, client: SMSClient, mocker: Any) -> None:
        fake_response = {
            "status": "1",
            "remarks": "Success",
            "error": "0",
            "total": "2",
            "contacts": [
                {"contactId": "123", "mobile": "306912345678", "name": "John"},
                {"contactId": "124", "mobile": "306912345678", "name": "Jane"},
            ],
        }

        call_mock = mocker.patch.object(
            client.contact,
            "call",
            return_value=fake_response,
        )

        response = client.contact.list()

        call_mock.assert_called_once_with(
            "GET",
            "contact/list",
        )

        assert response == fake_response

    def test_contract_get_calls_api(self, client: SMSClient, mocker: Any) -> None:
        fake_response = {
            "status": "1",
            "remarks": "Success",
            "error": "0",
            "contact": {"contactId": "123", "mobile": "306912345678", "name": "John", "smscost": "1"},
        }

        call_mock = mocker.patch.object(
            client.contact,
            "call",
            return_value=fake_response,
        )

        response = client.contact.get(contact_id="123")
        call_mock.assert_called_once_with(
            "GET",
            "contact/get",
            {"contactId": "123"},
        )
        assert response == fake_response

    @pytest.mark.parametrize(
        ("error_code", "error_message"),
        [
            ("214", "Error: No [contactId] parameter"),
            ("216", "Error: Error: [contactId:123456] not found"),
        ],
    )
    def test_contact_get_raises_on_error(
        self,
        client: SMSClient,
        mocker: Any,
        error_code: str,
        error_message: str,
    ) -> None:
        fake_response = {
            "status": "0",
            "error": error_code,
            "remarks": error_message,
        }

        mocker.patch.object(
            client.contact,
            "call",
            return_value=fake_response,
        )

        with pytest.raises(ContactExceptionError, match=re.escape(error_message)) as exc:
            client.contact.get(contact_id="123456")

        assert exc.value.code == error_code
        assert exc.value.args[0]

    def test_contact_update_calls_api(self, client: SMSClient, mocker: Any) -> None:
        fake_response = {
            "status": "1",
            "remarks": "Success",
            "error": "0",
            "contact": {"contactId": "123"},
        }

        call_mock = mocker.patch.object(
            client.contact,
            "call",
            return_value=fake_response,
        )

        response = client.contact.update(
            contact_id="123",
            name="John Updated",
        )

        call_mock.assert_called_once_with(
            "GET",
            "contact/update",
            {
                "contactId": "123",
                "name": "John Updated",
            },
        )

        assert response == fake_response

    def test_contact_update_filters_out_none_params(self, client: SMSClient, mocker: Any) -> None:
        fake_response = {
            "status": "1",
            "remarks": "Success",
            "error": "0",
            "contact": {"contactId": "123"},
        }

        call_mock = mocker.patch.object(client.contact, "call", return_value=fake_response)

        _ = client.contact.update(
            contact_id="123",
            mobile=None,
            name="John",
            surname=None,
            full_name=None,
            vname="V",
            vusername=None,
            birthday=None,
            nameday=None,
            custom1=None,
            custom2="X",
        )

        sent_params = call_mock.call_args.args[2]

        assert sent_params == {
            "contactId": "123",
            "name": "John",
            "vname": "V",
            "custom2": "X",
        }

    @pytest.mark.parametrize(
        ("error_code", "error_message"),
        [
            ("201", "Error: Parameter [mobile] cannot be parsed"),
            ("202", "Error: Contact already exists with this mobile"),
            ("203", "Error: Mobile number is Opt-out"),
            ("214", "Error: No [contactId] parameter"),
            ("221", "Error: Contact couldnt be updated"),
            ("0", "Failed"),
        ],
    )
    def test_contact_update_raises_on_error(
        self, client: SMSClient, mocker: Any, error_code: str, error_message: str
    ) -> None:
        fake_response = {
            "status": "0",
            "error": error_code,
            "remarks": error_message,
        }

        mocker.patch.object(
            client.contact,
            "call",
            return_value=fake_response,
        )

        with pytest.raises(ContactExceptionError, match=re.escape(error_message)) as exc:
            client.contact.update(
                contact_id="123",
            )

        assert exc.value.code == error_code
        assert exc.value.args[0]

    def test_contact_delete_calls_api(self, client: SMSClient, mocker: Any) -> None:
        fake_response = {
            "status": "1",
            "remarks": "Success",
            "error": "0",
        }

        call_mock = mocker.patch.object(
            client.contact,
            "call",
            return_value=fake_response,
        )

        response = client.contact.delete(contact_id="123")

        call_mock.assert_called_once_with(
            "GET",
            "contact/delete",
            {"contactId": "123"},
        )

        assert response == fake_response

    @pytest.mark.parametrize(
        ("error_code", "error_message"),
        [
            ("214", "Error: No [contactId] parameter"),
            ("216", "Error: Error: [contactId:123456] not found"),
        ],
    )
    def test_contact_delete_raises_on_error(
        self,
        client: SMSClient,
        mocker: Any,
        error_code: str,
        error_message: str,
    ) -> None:
        fake_response = {
            "status": "0",
            "error": error_code,
            "remarks": error_message,
        }

        mocker.patch.object(
            client.contact,
            "call",
            return_value=fake_response,
        )

        with pytest.raises(ContactExceptionError, match=re.escape(error_message)) as exc:
            client.contact.delete(contact_id="123456")

        assert exc.value.code == error_code
        assert exc.value.args[0]
