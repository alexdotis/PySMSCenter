from pysmscenter.types.base import BaseResponse


class BalanceRawData(BaseResponse, total=False):
    balance: str
