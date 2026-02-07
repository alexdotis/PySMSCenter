import typing
from datetime import date

from smsclient.exceptions import ContactExceptionError
from smsclient.utils import parse_date, raise_for_errors

from .manager import Manager

DateLike: typing.TypeAlias = str | date


class ContactID(typing.TypedDict):
    contactId: str


class ContactData(typing.TypedDict, total=False):
    status: typing.Literal["0", "1"]
    remarks: str
    error: str
    contact: ContactID


class Contacts(typing.TypedDict):
    contactId: str
    mobile: str
    smscost: str
    name: str
    surname: str
    vname: str
    birthday: str
    nameday: str
    custom1: str
    custom2: str


class ContactListData(typing.TypedDict, total=False):
    status: typing.Literal["0", "1"]
    remarks: str
    error: str
    total: str
    contacts: list[Contacts]


class Contact(typing.TypedDict):
    contactId: str
    mobile: str
    smscost: str
    name: str
    surname: str
    vname: str
    birthday: str
    nameday: str


class ContactDetail(typing.TypedDict, total=False):
    status: typing.Literal["0", "1"]
    remarks: str
    error: str
    total: str
    contact: Contact


class ContactDeleteData(typing.TypedDict, total=False):
    status: typing.Literal["0", "1"]
    remarks: str
    error: str


class ContactManager(Manager):
    name = "contact"

    def __str__(self) -> str:
        return self.__class__.__name__

    def add(
        self,
        mobile: str,
        name: str = "",
        surname: str = "",
        full_name: str = "",
        vname: str = "",
        vusername: str = "",
        birthday: DateLike | None = None,
        nameday: DateLike | None = None,
        **kwargs: typing.Any,
    ) -> ContactData:
        """Add a contact.

        Args:
            mobile (str): Mobile number of the contact
            name (str): Name of the contact
            surname (str): Surname of the contact
            full_name (str | None, optional): Fullname of contact. Defaults to None.
            vname (str | None, optional): First name in vocative. Useful for personalised messages. Defaults to None.
            vusername (str | None, optional): Last name in vocative. Useful for personalised messages. Defaults to None
            birthday (DateLike | None, optional): Birthday of contact in YYYY-MM-DD format. Defaults to None.
            nameday (DateLike | None, optional): Nameday of contact in YYYY-MM-DD format. Defaults to None.
            **kwargs: Additional API parameters to include.

        Raises:
            ContactExceptionError: If the API response indicates an error.

        Returns:
           ContactData: Response from the API.
        """
        params = {
            "mobile": mobile,
            "name": name,
            "surname": surname,
            "full_name": full_name,
            "vname": vname,
            "vusername": vusername,
            "birthday": self._date_to_api(birthday),
            "nameday": self._date_to_api(nameday),
            **kwargs,
        }

        response = self.call("GET", "contact/add", params)

        raise_for_errors(response, ContactExceptionError)

        return typing.cast(ContactData, response)

    def list(self) -> ContactListData:
        """Get the list of contacts.

        Raises:
            ContactExceptionError: If the API response indicates an error.

        Returns:
            ContactListData: Response from the API.
        """
        response = self.call("GET", "contact/list")
        return typing.cast(ContactListData, response)

    def get(self, contact_id: str) -> ContactDetail:
        """Get a contact's details.

        Args:
            contact_id: Contact ID to retrieve.

        Raises:
            ContactExceptionError: If the API response indicates an error.

        Returns:
            ContactDetail: Response from the API.
        """
        response = self.call("GET", "contact/get", {"contactId": contact_id})
        raise_for_errors(response, ContactExceptionError)
        return typing.cast(ContactDetail, response)

    def delete(self, contact_id: str) -> ContactDeleteData:
        """Delete a contact.

        Args:
            contact_id (str): Contact ID of the contact to delete.

        Raises:
            ContactExceptionError: If the API response indicates an error.

        Returns:
            ContactDeleteData: Response from the API.
        """

        response = self.call("GET", "contact/delete", {"contactId": contact_id})

        raise_for_errors(response, ContactExceptionError)

        return typing.cast(ContactDeleteData, response)

    def update(
        self,
        contact_id: str,
        mobile: str | None = None,
        name: str | None = None,
        surname: str | None = None,
        full_name: str | None = None,
        vname: str | None = None,
        vusername: str | None = None,
        birthday: DateLike | None = None,
        nameday: DateLike | None = None,
        **kwargs: typing.Any,
    ) -> ContactData:
        """Update a contact.

        Args:
            contact_id (str): Contact ID to update
            mobile (str | None, optional): Mobile number of the contact
            name (str | None, optional): Name of the contact
            surname (str | None, optional): Surname of the contact
            full_name (str | None, optional): Fullname of contact. Defaults to None.
            vname (str | None, optional): First name in vocative. Useful for personalised messages. Defaults to None.
            vusername (str | None, optional): Last name in vocative. Useful for personalised messages. Defaults to None
            birthday (DateLike | None, optional): Birthday of contact in YYYY-MM-DD format. Defaults to None.
            nameday (DateLike | None, optional): Nameday of contact in YYYY-MM-DD format. Defaults to None.
            **kwargs: Additional API parameters to include.

        Raises:
            ContactExceptionError: If the API response indicates an error.

        Returns:
            ContactData: Response from the API.
        """

        params = {
            "contactId": contact_id,
            "mobile": mobile,
            "name": name,
            "surname": surname,
            "full_name": full_name,
            "vname": vname,
            "vusername": vusername,
            "birthday": self._date_to_api(birthday),
            "nameday": self._date_to_api(nameday),
            **kwargs,
        }
        params = {key: value for key, value in params.items() if value is not None}
        response = self.call("GET", "contact/update", params)

        raise_for_errors(response, ContactExceptionError)

        return typing.cast(ContactData, response)

    @staticmethod
    def _date_to_api(value: date | str | None) -> str | None:
        """Convert a date-like value to the API's date string.

        Args:
            value: Date or ISO-like string.

        Returns:
            ISO-8601 date string, or None if value is None.

        Raises:
            ContactExceptionError: If the date string cannot be parsed.
        """
        if value is None:
            return None

        if isinstance(value, date):
            return value.isoformat()
        try:
            return parse_date(value).isoformat()
        except ValueError as exc:
            raise ContactExceptionError(str(exc)) from exc
