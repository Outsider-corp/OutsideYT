class OutsideError(Exception):
    """Base pytube exception that all others inherit."""


class MaxRetriesError(OutsideError):
    """Maximum number of retries exceeded."""

class RequestMethodTypeError(OutsideError):
    """Unable method for request"""
