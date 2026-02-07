import typing

from smsclient.exceptions import GroupExceptionError
from smsclient.utils import raise_for_errors

from .manager import Manager


class Group(typing.TypedDict):
    groupId: str


class GroupList(typing.TypedDict):
    groupId: str
    name: str


class GroupData(typing.TypedDict, total=False):
    status: typing.Literal["0", "1"]
    remarks: str
    error: str
    group: Group


class GroupListData(typing.TypedDict, total=False):
    status: typing.Literal["0", "1"]
    remarks: str
    error: str
    total: str
    groups: list[GroupList]


class GroupContact(typing.TypedDict, total=False):
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


class GroupGetGroup(typing.TypedDict, total=False):
    name: str
    total: str
    contacts: list[GroupContact]


class GroupGetData(typing.TypedDict, total=False):
    status: typing.Literal["0", "1"]
    remarks: str
    error: str
    total: str
    group: GroupGetGroup


class GroupContactLink(typing.TypedDict):
    contactGroupId: str


class GroupAddContactGroup(typing.TypedDict):
    contact: GroupContactLink


class GroupAddContactData(typing.TypedDict, total=False):
    status: typing.Literal["0", "1"]
    remarks: str
    error: str
    group: GroupAddContactGroup


class GroupDeleteContactData(typing.TypedDict, total=False):
    status: typing.Literal["0", "1"]
    remarks: str
    error: str


class GroupManager(Manager):
    name = "group"

    def __str__(self) -> str:
        return self.__class__.__name__

    def add(self, name: str) -> GroupData:
        """
        Add a new group.

        Args:
            name (str): The name of the group to be added.
        """

        response = self.call("GET", "group/add", {"name": name})
        raise_for_errors(response, GroupExceptionError)
        return typing.cast(GroupData, response)

    def delete(self, group_id: str) -> GroupData:
        """
        Delete a group.

        Args:
            group_id (str): The ID of the group to be deleted.
        """

        response = self.call("GET", "group/delete", {"groupId": group_id})
        raise_for_errors(response, GroupExceptionError)

        return typing.cast(GroupData, response)

    def list(self) -> GroupListData:
        """
        List all groups.

        Returns:
            GroupData: Response from the API.
        """

        response = self.call("GET", "group/list")

        return typing.cast(GroupListData, response)

    def get(self, group_id: str) -> GroupGetData:
        """
        Get details of a specific group.

        Args:
            group_id (str): The ID of the group to retrieve.

        Raises:
            GroupExceptionError: If the API response indicates an error.

        Returns:
            GroupGetData: Response from the API.
        """

        response = self.call("GET", "group/get", {"groupId": group_id})

        raise_for_errors(response, GroupExceptionError)

        return typing.cast(GroupGetData, response)

    def add_contact(self, group_id: str, contact_id: str) -> GroupAddContactData:
        """
        Add a contact to a group.

        Args:
            group_id (str): The ID of the group to which the contact will be added.
            contact_id (str): The ID of the contact to be added.

        Raises:
            GroupExceptionError: If the API response indicates an error.

        Returns:
            GroupAddContactData: Response from the API.
        """
        params = {
            "groupId": group_id,
            "contactId": contact_id,
        }

        response = self.call("GET", "group/addContact", params)

        raise_for_errors(response, GroupExceptionError)

        return typing.cast(GroupAddContactData, response)

    @typing.overload
    def delete_contact(self, *, group_id: str, contact_id: str) -> GroupDeleteContactData: ...

    @typing.overload
    def delete_contact(self, *, contact_group_id: str) -> GroupDeleteContactData: ...

    def delete_contact(
        self,
        *,
        group_id: str | None = None,
        contact_id: str | None = None,
        contact_group_id: str | None = None,
    ) -> GroupDeleteContactData:
        """
        Delete a contact from a group.

        Args:
            group_id (str, optional): The ID of the group from which the contact will be deleted. Required
            if contact_group_id is not provided.
            contact_id (str, optional): The ID of the contact to be deleted. Required
            if contact_group_id is not provided.
            contact_group_id (str, optional): The ID of the contact-group link to be deleted. Required
            if group_id and contact_id are not provided.
        Raises:
            GroupExceptionError: If the API response indicates an error.
            ValueError: If neither contact_group_id nor both group_id and contact_id are provided.
        Returns:
            GroupDeleteContactData: Response from the API.
        """
        error_message = "Either contact_group_id or both group_id and contact_id must be provided."

        has_group_and_contact = group_id is not None and contact_id is not None
        has_contact_group_id = contact_group_id is not None
        has_any_group_contact = group_id is not None or contact_id is not None

        if not has_group_and_contact and not has_contact_group_id:
            raise ValueError(error_message)

        if has_contact_group_id and has_any_group_contact:
            raise ValueError(error_message)

        if contact_group_id is not None:
            params = {"contactGroupId": contact_group_id}
        else:
            params = {
                "groupId": group_id,
                "contactId": contact_id,
            }

        response = self.call("GET", "group/deleteContact", params)

        raise_for_errors(response, GroupExceptionError)

        return typing.cast(GroupDeleteContactData, response)

    def delete_all_contacts(self, group_id: str) -> GroupDeleteContactData:
        """
        Delete all contacts from a group.

        Args:
            group_id (str): The ID of the group from which all contacts will be deleted.
        Raises:
            GroupExceptionError: If the API response indicates an error.
        Returns:
            GroupDeleteContactData: Response from the API.
        """
        response = self.call("GET", "group/deleteAllContacts", {"groupId": group_id})

        raise_for_errors(response, GroupExceptionError)

        return typing.cast(GroupDeleteContactData, response)
