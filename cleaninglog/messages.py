"""WSGI Messages."""

from his import Message


class _CleaningLogMessage(Message):
    """Abstract base message."""

    LOCALES = '/etc/his.d/locale/cleaninglog.ini'


class NoSuchTerminal(_CleaningLogMessage):
    """Indicates that the respective terminal does not exist."""

    STATUS = 404


class NoSuchUser(_CleaningLogMessage):
    """Indicates that the respective user does not exist."""

    STATUS = 404


class TerminalUnlocated(_CleaningLogMessage):
    """Indicates that the respective terminal has no location assigned."""

    STATUS = 404
