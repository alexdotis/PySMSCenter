from typing import cast

from smsclient.types.key_types import KeyRawResponse

from .manager import Manager


class KeyManager(Manager):
    name = "key"

    def __str__(self) -> str:
        return self.__class__.__name__

    def get(self, username: str, password: str) -> KeyRawResponse:
        """
        Get an API key for the given username and password.

        Args:
            username (str): The username to authenticate with.
            password (str): The password to authenticate with.
        Returns:
            KeyRawResponse: The API key for the authenticated user.
        """
        response = self.call("GET", "key/get", params={"username": username, "password": password})
        return cast(KeyRawResponse, response)

    def reset(self, username: str, password: str) -> KeyRawResponse:
        """
        Reset the API key for the authenticated user.

        Returns:
            KeyRawResponse: The new API key for the authenticated user.
        """

        response = self.call("GET", "key/reset", params={"username": username, "password": password})
        return cast(KeyRawResponse, response)
