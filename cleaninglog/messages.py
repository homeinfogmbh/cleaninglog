"""WSGI Messages."""

from wsgilib import JSONMessage


__all__ = ['NO_SUCH_SYSTEM', 'NO_SUCH_USER', 'SYSTEM_NOT_LOCATED']


NO_SUCH_SYSTEM = JSONMessage(
    'The requested system does not exist.', status=404)
NO_SUCH_USER = JSONMessage('The requested user does not exist.', status=404)
SYSTEM_NOT_LOCATED = JSONMessage(
    'The requested system does not have an address.', status=400)
