"""WSGI Messages."""

from his import HIS_MESSAGE_FACILITY


__all__ = ['NO_SUCH_TERMINAL', 'NO_SUCH_USER', 'TERMINAL_NOT_LOCATED']


CLEANING_LOG_MESSAGE_DOMAIN = HIS_MESSAGE_FACILITY.domain('cleaninglog')
CLEANING_LOG_MESSAGE = CLEANING_LOG_MESSAGE_DOMAIN.message
NO_SUCH_TERMINAL = CLEANING_LOG_MESSAGE(
    'The requested terminal does not exist.', status=404)
NO_SUCH_USER = CLEANING_LOG_MESSAGE(
    'The requested user does not exist.', status=404)
TERMINAL_NOT_LOCATED = CLEANING_LOG_MESSAGE(
    'The requested terminal does not have an address.', status=400)
