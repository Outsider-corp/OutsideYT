class OutsideError(BaseException):
    """Base pytube exception that all others inherit."""


class MaxRetriesError(OutsideError):
    """Maximum number of retries exceeded."""


class RequestMethodTypeError(OutsideError):
    """Unable method for request"""


class StatusCodeRequestError(OutsideError):
    """Status Code of request is not 200"""

    def __init__(self, reason=None):
        print(f'{reason}')


class StopThreadError(OutsideError):
    """Thread was stopped."""


class BrowserClosedError(OutsideError):
    """Browser was closed."""


class NotFoundCookiesError(OutsideError):
    """Cookies for user not found."""

    def __init__(self, file_cookies: str):
        self.cookies = file_cookies


class OutdatedCookiesError(OutsideError):
    """Cookies files are outdated."""

    def __init__(self, user: str):
        self.user = user
