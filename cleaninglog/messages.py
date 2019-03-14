"""WSGI Messages."""

from wsgilib import JSONMessage


__all__ = ['NO_SUCH_TERMINAL', 'NO_SUCH_USER', 'TERMINAL_NOT_LOCATED']


NO_SUCH_TERMINAL = JSONMessage(
    'The requested terminal does not exist.', status=404)
NO_SUCH_USER = JSONMessage('The requested user does not exist.', status=404)
TERMINAL_NOT_LOCATED = JSONMessage(
    'The requested terminal does not have an address.', status=400)
