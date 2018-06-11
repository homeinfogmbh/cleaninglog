"""Common WSGI functions."""

from cleaninglog.messages import TerminalUnlocated

__all__ = ['get_address']


def get_address(terminal):
    """Returns the terminal's address."""

    try:
        return terminal.location.address
    except AttributeError:
        return TerminalUnlocated()
