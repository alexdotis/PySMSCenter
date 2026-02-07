from typing import Literal, TypedDict


class BaseResponse(TypedDict):
    status: Literal["0", "1"]
    remarks: str
    error: str
