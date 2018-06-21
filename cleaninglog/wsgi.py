"""Authenticated and authorized HIS services."""

from datetime import datetime

from flask import request

from his import CUSTOMER, authenticated, authorized, Application
from his.messages import NotAnInteger
from terminallib import Terminal
from timelib import strpdatetime
from wsgilib import JSON

from cleaninglog.messages import NoSuchUser, NoSuchTerminal, TerminalUnlocated
from digsigdb import CleaningUser, CleaningDate

__all__ = ['APPLICATION']


APPLICATION = Application('Cleaning Log', cors=True, debug=True)


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
            & _cleaning_user_selects()).get()
    except CleaningUser.DoesNotExist:
        raise NoSuchUser()


def _terminal(tid):
    """Returns the respective terminal."""

    try:
        return Terminal.select().where(
            (Terminal.tid == tid) & (Terminal.customer == CUSTOMER.id)).get()
    except Terminal.DoesNotExist:
        raise NoSuchTerminal()


def _address(terminal):
    """Returns the terminal's address."""

    try:
        return terminal.location.address
    except AttributeError:
        return TerminalUnlocated()


def _entries(since, until, user=None, address=None):
    """Yields the respective customer's entries."""

    if user is None:
        expression = CleaningDate.user << [user.id for user in _users()]
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

    return JSON([user.to_dict() for user in _users()])


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
        return NotAnInteger()
    else:
        user = _user(user)

    try:
        tid = int(request.args['terminal'])
    except KeyError:
        address = None
    except (ValueError, TypeError):
        return NotAnInteger()
    else:
        address = _address(_terminal(tid))

    entries = _entries(since, until, user=user, address=address)
    return JSON([entry.to_dict() for entry in entries])


ROUTES = (
    ('GET', '/', list_entries, 'list_entries'),
    ('GET', '/users', list_users, 'list_users'))
APPLICATION.add_routes(ROUTES)
