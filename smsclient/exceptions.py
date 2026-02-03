class SMSClientError(Exception):
    pass


class CrendetialError(SMSClientError):
    pass


class SMSExceptionError(SMSClientError):
    pass


class ContactExceptionError(SMSClientError):
    pass


class MobileExceptionError(SMSClientError):
    pass
