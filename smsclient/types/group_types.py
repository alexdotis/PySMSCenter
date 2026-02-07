from typing import TypedDict

from smsclient.types.base import BaseResponse


class Group(TypedDict):
    groupId: str


class GroupList(TypedDict):
    groupId: str
    name: str


class GroupData(BaseResponse, total=False):
    group: Group


class GroupListData(BaseResponse, total=False):
    total: str
    groups: list[GroupList]


class GroupContact(TypedDict, total=False):
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


class GroupGetGroup(TypedDict, total=False):
    name: str
    total: str
    contacts: list[GroupContact]


class GroupGetData(BaseResponse, total=False):
    total: str
    group: GroupGetGroup


class GroupContactLink(TypedDict):
    contactGroupId: str


class GroupAddContactGroup(TypedDict):
    contact: GroupContactLink


class GroupAddContactData(BaseResponse, total=False):
    group: GroupAddContactGroup
