"""WSGI Messages."""

from his import Message


__all__ = ['NoSuchTerminal', 'NoSuchUser', 'TerminalUnlocated']


class _CleaningLogMessage(Message):
    """Abstract base message."""

    DOMAIN = 'cleaninglog'


class NoSuchTerminal(_CleaningLogMessage):
    """Indicates that the respective terminal does not exist."""

    STATUS = 404


class NoSuchUser(_CleaningLogMessage):
    """Indicates that the respective user does not exist."""

    STATUS = 404


class TerminalUnlocated(_CleaningLogMessage):
    """Indicates that the respective terminal has no location assigned."""

    STATUS = 404
