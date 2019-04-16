"""Authenticated and authorized HIS services."""

from datetime import datetime

from flask import request

from digsigdb import CleaningUser, CleaningDate
from his import CUSTOMER, authenticated, authorized, Application
from his.messages.data import NOT_AN_INTEGER
from terminallib import Deployment, System
from timelib import strpdatetime
from wsgilib import JSON

from cleaninglog.messages import NO_SUCH_SYSTEM
from cleaninglog.messages import NO_SUCH_USER
from cleaninglog.messages import SYSTEM_NOT_DEPLOYED


__all__ = ['APPLICATION']


APPLICATION = Application('Cleaning Log', debug=True)


def _cleaning_user_selects():
    """Returns a basic expression for cleaning users selection."""

    return (
        (CleaningUser.created < datetime.now())
        & (CleaningUser.enabled == 1))


def _users():
    """Yields the customer's users."""

    return CleaningUser.select().where(
        (CleaningUser.customer == CUSTOMER.id) & _cleaning_user_selects())


def _user(ident):
    """Returns the respective user."""

    try:
        return CleaningUser.select().where(
            (CleaningUser.id == ident)
            & (CleaningUser.customer == CUSTOMER.id)
            & _cleaning_user_selects()
        ).get()
    except CleaningUser.DoesNotExist:
        raise NO_SUCH_USER


def _system(ident):
    """Returns the respective system."""

    try:
        return System.select().join(Deployment).where(
            (System.id == ident)
            & (Deployment.customer == CUSTOMER.id)
        ).get()
    except System.DoesNotExist:
        raise NO_SUCH_SYSTEM


def _address(system):
    """Returns the system's address."""

    deployment = system.deployment

    if deployment is None:
        return SYSTEM_NOT_DEPLOYED

    return deployment.address


def _entries(since, until, user=None, address=None):
    """Yields the respective customer's entries."""

    if user is None:
        expression = CleaningDate.user << {user.id for user in _users()}
    else:
        expression = CleaningDate.user == user

    if address is not None:
        expression &= CleaningDate.address == address

    if since is not None:
        expression &= CleaningDate.timestamp >= since

    if until is not None:
        expression &= CleaningDate.timestamp <= until

    return CleaningDate.select().where(expression)


@authenticated
@authorized('cleaninglog')
def list_users():
    """Lists the cleaning log users of the respective customer."""

    return JSON([user.to_json() for user in _users()])


@authenticated
@authorized('cleaninglog')
def list_entries():
    """Lists the cleaning log entries of the respective customer."""

    since = strpdatetime(request.args.get('since'))
    until = strpdatetime(request.args.get('until'))

    try:
        user = int(request.args['user'])
    except KeyError:
        user = None
    except (ValueError, TypeError):
        return NOT_AN_INTEGER
    else:
        user = _user(user)

    try:
        system = int(request.args['system'])
    except KeyError:
        address = None
    except (ValueError, TypeError):
        return NOT_AN_INTEGER
    else:
        address = _address(_system(system))

    entries = _entries(since, until, user=user, address=address)
    return JSON([entry.to_json() for entry in entries])


ROUTES = (
    ('GET', '/', list_entries, 'list_entries'),
    ('GET', '/users', list_users, 'list_users'))
APPLICATION.add_routes(ROUTES)
