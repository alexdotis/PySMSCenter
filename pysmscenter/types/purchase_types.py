from typing import TypedDict

from .base import BaseResponse


class PurchaseItem(TypedDict):
    purchaseId: str
    timestamp: str
    cost: str
    sms: str


class PurchaseRawResponse(BaseResponse, total=False):
    purchases: list[PurchaseItem]
