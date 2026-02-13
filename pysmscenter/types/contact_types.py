from datetime import date
from typing import TypedDict

from pysmscenter.types.base import BaseResponse

type DateLike = str | date


class ContactID(TypedDict):
    contactId: str


class ContactData(BaseResponse, total=False):
    contact: ContactID


class Contacts(TypedDict):
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


class ContactListData(BaseResponse, total=False):
    total: str
    contacts: list[Contacts]


class Contact(TypedDict):
    contactId: str
    mobile: str
    smscost: str
    name: str
    surname: str
    vname: str
    birthday: str
    nameday: str


class ContactDetail(BaseResponse, total=False):
    total: str
    contact: Contact
