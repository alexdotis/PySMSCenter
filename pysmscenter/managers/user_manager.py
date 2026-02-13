from typing import cast

from email_validator import EmailNotValidError, validate_email

from pysmscenter.exceptions import SMSClientError, UserCommentExceptionError, UserExceptionError
from pysmscenter.types import (
    BaseResponse,
    UserCommentListRawResponseType,
    UserCommentRawResponse,
    UserListRawResponseType,
    UserRawResponse,
)
from pysmscenter.utils import raise_for_errors

from .manager import Manager


class UserManager(Manager):
    name = "user"

    def __str__(self) -> str:
        return self.__class__.__name__

    def add(self, email: str, password: str) -> UserRawResponse:
        """
        Add a new sub-account with the given email and password.

        Args:
            email (str): The email address for the new sub-account.
            password (str): The password for the new sub-account.

        """

        self._validate_email(email)
        params = {"email": email, "password": password}
        response = self.call("GET", "user/add", params=params)
        raise_for_errors(response, UserExceptionError)
        return cast(UserRawResponse, response)

    def delete(self, user_id: str) -> None:
        """
        Delete a sub-account by its user ID.

        Args:
            user_id (str): The ID of the sub-account to delete.
        """
        raise NotImplementedError("The delete user endpoint is not implemented in the API documentation.")

    def email(self) -> None:
        raise NotImplementedError("The email user endpoint is not implemented in the API documentation.")

    def email_all(self) -> None:
        raise NotImplementedError("The email all users endpoint is not implemented in the API documentation.")

    def get(self) -> None:
        raise NotImplementedError("The get user endpoint is not implemented in the API documentation.")

    def sms(self) -> None:
        raise NotImplementedError("The get user SMS endpoint is not implemented in the API documentation.")

    def sms_all(self) -> None:
        raise NotImplementedError("The get all users SMS endpoint is not implemented in the API documentation.")

    def update(self) -> None:
        raise NotImplementedError("The update user endpoint is not implemented in the API documentation.")

    def list(self) -> UserListRawResponseType:
        """
        List all sub-accounts under the main account.

        Returns:
            UserListRawResponseType: The response containing the list of sub-accounts.
        """
        response = self.call("GET", "user/list")
        return cast(UserListRawResponseType, response)

    def topup(self, user_id: str, sms: str, cost: str) -> UserRawResponse:
        """
        Top up a sub-account with the specified amount.

        Args:
            user_id (str): The ID of the sub-account to top up.
            sms (str): The number of SMS to add to the sub-account balance.
            cost (str): The cost associated with the top-up.

        Returns:
            UserRawResponse: The response containing the updated sub-account information.
        """
        params = {"userId": user_id, "sms": sms, "cost": cost}
        response = self.call("GET", "user/topup", params=params)
        raise_for_errors(response, UserExceptionError)
        return cast(UserRawResponse, response)

    def add_comment(self, user_id: str, comment: str) -> UserCommentRawResponse:
        """
        Add a comment to a sub-account.

        Args:
            user_id (str): The ID of the sub-account to add a comment to.
            comment (str): The comment to add to the sub-account.
        """
        params = {"userId": user_id, "comment": comment}
        response = self.call("GET", "user/comment/add", params=params)
        raise_for_errors(response, UserCommentExceptionError)
        return cast(UserCommentRawResponse, response)

    def delete_comment(self, comment_id: str) -> BaseResponse:
        """
        Delete a comment from a sub-account.

        Args:
            comment_id (str): The ID of the comment to delete.
        """
        params = {"commentId": comment_id}
        response = self.call("GET", "user/comment/delete", params=params)
        raise_for_errors(response, SMSClientError)
        return cast(BaseResponse, response)

    def comments(self, user_id: str) -> UserCommentListRawResponseType:
        """
        List all comments for a sub-account.

        Args:
            user_id (str): The ID of the sub-account to list comments for.
        """
        params = {"userId": user_id}
        response = self.call("GET", "user/comment/list", params=params)
        raise_for_errors(response, SMSClientError)
        return cast(UserCommentListRawResponseType, response)

    @staticmethod
    def _validate_email(email: str) -> None:
        """
        Validate an email address.

        Args:
            email (str): The email address to validate.

        Returns:
            None
        """
        try:
            validate_email(email)
        except EmailNotValidError as e:
            raise ValueError(f"Invalid email address: {email}") from e
