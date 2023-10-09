class OutsideError(Exception):
    """Base pytube exception that all others inherit."""


class MaxRetriesError(OutsideError):
    """Maximum number of retries exceeded."""

class RequestMethodTypeError(OutsideError):
    """Unable method for request"""

class StatusCodeRequestError(OutsideError):
    """Status Code of request is not 200"""
    def __init__(self, reason):
        print(f'{reason}')
