from typing import TypedDict

from .base import BaseResponse


class UserItem(TypedDict):
    userId: str
    balance: int


class UserRawResponse(BaseResponse, total=False):
    user: UserItem


class UserListItem(TypedDict, total=False):
    userId: str
    username: str
    email: str
    balance: str
    mobile: str
    key: str | None


class UserListRawResponse(BaseResponse, total=False):
    total: str


type UserListRawResponseType = dict[str, UserListItem | str]


class CommentItem(TypedDict):
    commentId: str


class UserCommentRawResponse(BaseResponse, total=False):
    comment: CommentItem


class UserCommentListItem(TypedDict):
    commentId: str
    comment: str
    timestamp: str


class UserCommentListRawResponseType(BaseResponse, total=False):
    total: str
    comments: list[UserCommentListItem]
