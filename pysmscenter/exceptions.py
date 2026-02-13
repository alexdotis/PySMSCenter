import typing


class SMSClientError(Exception):
    def __init__(
        self, message: str | None = None, code: str | None = None, response: dict[str, typing.Any] | None = None
    ) -> None:
        self.message = message
        self.code = code
        self.response = response
        super().__init__(message)

    def __str__(self) -> str:
        msg = super().__str__()
        return f"[{self.code}] {msg}" if self.code and msg else (f"[{self.code}]" if self.code else msg)


class CredentialError(SMSClientError):
    pass


class SMSExceptionError(SMSClientError):
    pass


class ContactExceptionError(SMSClientError):
    pass


class MobileExceptionError(SMSClientError):
    pass


class GroupExceptionError(SMSClientError):
    pass


class HLRExceptionError(SMSClientError):
    pass


class TwoFactorExceptionError(SMSClientError):
    pass


class UserExceptionError(SMSClientError):
    pass


class UserCommentExceptionError(SMSClientError):
    pass
