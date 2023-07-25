"""Common exceptions."""


__all__ = ["DuplicateUserError"]


class DuplicateUserError(Exception):
    """Indicates that a respective cleaning user already exists."""
