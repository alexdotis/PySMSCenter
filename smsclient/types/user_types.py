from typing import TypedDict

from .base import BaseResponse


class UserItem(TypedDict):
    userId: str
    balance: str


class UserRawResponse(BaseResponse, total=False):
    user: UserItem
