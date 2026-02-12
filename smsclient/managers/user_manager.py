from typing import cast

from email_validator import EmailNotValidError, validate_email

from smsclient.exceptions import UserExceptionError
from smsclient.types import UserRawResponse
from smsclient.utils import raise_for_errors

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

    def list(self) -> UserRawResponse:
        """
        List all sub-accounts under the main account.

        Returns:
            UserRawResponse: The response containing the list of sub-accounts.
        """
        response = self.call("GET", "user/list")
        raise_for_errors(response, UserExceptionError)
        return cast(UserRawResponse, response)

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
