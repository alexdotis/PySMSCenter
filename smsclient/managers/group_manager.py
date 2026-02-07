from typing import cast, overload

from smsclient.exceptions import GroupExceptionError
from smsclient.types import BaseResponse, GroupAddContactData, GroupData, GroupGetData, GroupListData
from smsclient.utils import raise_for_errors

from .manager import Manager


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
        return cast(GroupData, response)

    def delete(self, group_id: str) -> GroupData:
        """
        Delete a group.

        Args:
            group_id (str): The ID of the group to be deleted.
        """

        response = self.call("GET", "group/delete", {"groupId": group_id})
        raise_for_errors(response, GroupExceptionError)

        return cast(GroupData, response)

    def list(self) -> GroupListData:
        """
        List all groups.

        Returns:
            GroupData: Response from the API.
        """

        response = self.call("GET", "group/list")

        return cast(GroupListData, response)

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

        return cast(GroupGetData, response)

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

        return cast(GroupAddContactData, response)

    @overload
    def delete_contact(self, *, group_id: str, contact_id: str) -> BaseResponse: ...

    @overload
    def delete_contact(self, *, contact_group_id: str) -> BaseResponse: ...

    def delete_contact(
        self,
        *,
        group_id: str | None = None,
        contact_id: str | None = None,
        contact_group_id: str | None = None,
    ) -> BaseResponse:
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
            BaseResponse: Response from the API.
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

        return cast(BaseResponse, response)

    def delete_all_contacts(self, group_id: str) -> BaseResponse:
        """
        Delete all contacts from a group.

        Args:
            group_id (str): The ID of the group from which all contacts will be deleted.
        Raises:
            GroupExceptionError: If the API response indicates an error.
        Returns:
            BaseResponse: Response from the API.
        """
        response = self.call("GET", "group/deleteAllContacts", {"groupId": group_id})

        raise_for_errors(response, GroupExceptionError)

        return cast(BaseResponse, response)
