import typing
from datetime import date

from exceptions import ContactExceptionError
from smsclient.utils import raise_for_errors

from .manager import Manager


class ContactID(typing.TypedDict):
    contactId: str


class ContactData(typing.TypedDict):
    status: str
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


class ContactListData(typing.TypedDict):
    status: str
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


class ContactDetail(typing.TypedDict):
    status: str
    remarks: str
    error: str
    total: str
    contact: Contact


class ContactDeleteData(typing.TypedDict):
    status: str
    remarks: str
    error: str


class ContactManager(Manager):
    name = "contact"

    def __str__(self) -> str:
        return self.__class__.__name__

    def add(
        self,
        mobile: str,
        name: str,
        surname: str,
        full_name: str = "",
        vname: str = "",
        vusername: str = "",
        birthday: date | None = None,
        nameday: date | None = None,
        **kwargs: typing.Any,
    ) -> ContactData:
        """Add a contact

        Args:
            mobile (str): Mobile number of the contact
            name (str): Name of the contact
            surname (str): Surname of the contact
            full_name (str | None, optional): Fullname of contact. Defaults to None.
            vname (str | None, optional): First name in vocative. Useful for personalised messages. Defaults to None.
            vusername (str | None, optional): Last name in vocative. Useful for personalised messages. Defaults to None
            birthday (date | None, optional): Birthday of contact in YYYY-MM-DD format. Defaults to None.
            nameday (date | None, optional): Nameday of contact in YYYY-MM-DD format. Defaults to None.

        Raises:
            ContactExceptionError:

        Returns:
           ContactData: Response from the API
        """
        params = {
            "mobile": mobile,
            "name": name,
            "surname": surname,
            "full_name": full_name,
            "vname": vname,
            "vusername": vusername,
            "birthday": birthday,
            "nameday": nameday,
            **kwargs,
        }

        response = self.call("GET", "contact/add", params)
        error_codes = {"201", "202", "203", "204", "205"}

        raise_for_errors(response, error_codes, ContactExceptionError)

        return typing.cast(ContactData, response)

    def list(self) -> ContactListData:
        """Get the list of contacts

        Raises:
            ContactExceptionError: If error code is in error_codes

        Returns:
            ContactListData: Response from the API
        """
        response = self.call("GET", "contact/list", {"type": "json"})
        return typing.cast(ContactListData, response)

    def get(self, contact_id: str) -> ContactDetail:
        """Get the list of contacts

        Raises:
            ContactExceptionError: If error code is in error_codes

        Returns:
            ContactDetail: Response from the API
        """
        error_codes = {"214", "216"}
        response = self.call("GET", "contact/get", {"contactId": contact_id, "type": "json"})
        raise_for_errors(response, error_codes, ContactExceptionError)
        return typing.cast(ContactDetail, response)

    def delete(self, contact_id: str) -> ContactDeleteData:
        """Delete a contact

        Args:
            mobile (str): Mobile number of the contact to delete

        Raises:
            ContactExceptionError: If error code is in error_codes

        Returns:
            ContactDeleteData: Response from the API
        """

        response = self.call("GET", "contact/delete", {"contactId": contact_id, "type": "json"})
        error_codes = {"214", "216"}

        raise_for_errors(response, error_codes, ContactExceptionError)

        return typing.cast(ContactDeleteData, response)

    def update(
        self,
        contact_id: str,
        mobile: str,
        name: str,
        surname: str,
        full_name: str = "",
        vname: str = "",
        vusername: str = "",
        birthday: date | None = None,
        nameday: date | None = None,
        **kwargs: typing.Any,
    ) -> ContactData:
        """_summary_

        Args:
            contact_id (str): Contact ID to update
            mobile (str): Mobile number of the contact
            name (str): Name of the contact
            surname (str): Surname of the contact
            full_name (str | None, optional): Fullname of contact. Defaults to None.
            vname (str | None, optional): First name in vocative. Useful for personalised messages. Defaults to None.
            vusername (str | None, optional): Last name in vocative. Useful for personalised messages. Defaults to None
            birthday (date | None, optional): Birthday of contact in YYYY-MM-DD format. Defaults to None.
            nameday (date | None, optional): Nameday of contact in YYYY-MM-DD format. Defaults to None.

        Raises:
            ContactExceptionError: _description_

        Returns:
            ContactData: _description_
        """

        params = {
            "contactId": contact_id,
            "mobile": mobile,
            "name": name,
            "surname": surname,
            "full_name": full_name,
            "vname": vname,
            "vusername": vusername,
            "birthday": birthday,
            "nameday": nameday,
            **kwargs,
        }

        response = self.call("GET", "contact/update", params)
        error_codes = {"201", "202", "203", "214", "221"}

        raise_for_errors(response, error_codes, ContactExceptionError)

        return typing.cast(ContactData, response)
