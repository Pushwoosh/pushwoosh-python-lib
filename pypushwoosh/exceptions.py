class PushwooshException(Exception):
    pass


class PushwooshCommandException(PushwooshException):
    pass


class PushwooshNotificationException(PushwooshException):
    pass


class PushwooshFilterException(PushwooshException):
    pass


class PushwooshFilterInvalidOperatorException(PushwooshFilterException):
    pass


class PushwooshFilterInvalidOperandException(PushwooshFilterException):
    pass
