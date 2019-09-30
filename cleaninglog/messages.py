"""WSGI Messages."""

from wsgilib import JSONMessage


__all__ = [
    'CLEANING_DATE_CREATED',
    'CLEANING_DATE_DELETED',
    'CLEANING_DATE_PATCHED',
    'NO_DEPLOYMENT_SPECIFIED',
    'NO_SUCH_CLEANING_DATE',
    'NO_SUCH_DEPLOYMENT',
    'NO_SUCH_SYSTEM',
    'NO_SUCH_USER',
    'NO_USER_SPECIFIED',
    'SYSTEM_NOT_DEPLOYED'
]


CLEANING_DATE_CREATED = JSONMessage('Cleaning date created.', status=201)
CLEANING_DATE_DELETED = JSONMessage('Cleaning date created.', status=200)
CLEANING_DATE_PATCHED = JSONMessage('Cleaning date created.', status=200)
NO_DEPLOYMENT_SPECIFIED = JSONMessage('No deployment specified.', status=400)
NO_SUCH_CLEANING_DATE = JSONMessage('No such cleaning date.', status=404)
NO_SUCH_DEPLOYMENT = JSONMessage('No such deployment.', status=404)
NO_SUCH_SYSTEM = JSONMessage('No such system.', status=404)
NO_SUCH_USER = JSONMessage('No such user.', status=404)
NO_USER_SPECIFIED = JSONMessage('No user specified.', status=400)
SYSTEM_NOT_DEPLOYED = JSONMessage(
    'The requested system is not deployed.', status=400)
