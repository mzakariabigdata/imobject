""" exception Module """


class BaseError(Exception):
    """Base Exception"""


class BaseNotFound(BaseError):
    """Base not found excetion"""


class BaseMultipleFound(BaseError):
    """Base multiple found excetion"""
