"""Authenticated and authorized HIS services."""

from flask import request

from his import CUSTOMER, authenticated, authorized, Application
from his.messages import NotAnInteger
from terminallib import Terminal
from timelib import strpdatetime
from wsgilib import JSON

from cleaninglog.messages import NoSuchUser, NoSuchTerminal
from cleaninglog.orm import User, Log
from cleaninglog.wsgi.common import get_address


APPLICATION = Application('Cleaning Log', cors=True, debug=True)


def _users():
    """Yields the customer's users."""

    return User.select().where(User.customer == CUSTOMER.id)


def _user(ident):
    """Returns the respective user."""

    try:
        return User.select().where(
            (User.id == ident) & (User.customer == CUSTOMER.id)).get()
    except User.DoesNotExist:
        raise NoSuchUser()


def _terminal(tid):
    """Returns the respective terminal."""

    try:
        return Terminal.select().where(
            (Terminal.tid == tid) & (Terminal.customer == CUSTOMER.id)).get()
    except Terminal.DoesNotExist:
        raise NoSuchTerminal()


def _entries(start, end, user=None, address=None):
    """Yields the respective customer's entries."""

    if user is None:
        expression = Log.user << [user.id for user in _users()]
    else:
        expression = Log.user == user

    if address is not None:
        expression &= Log.address == address

    if start is not None:
        expression &= Log.timestamp >= start

    if end is not None:
        expression &= Log.timestamp <= end

    return Log.select().where(expression)


@authenticated
@authorized('cleaninglog')
def list_users():
    """Lists the cleaning log users of the respective customer."""

    return JSON([user.to_dict() for user in _users()])


@authenticated
@authorized('cleaninglog')
def list_entries():
    """Lists the cleaning log entries of the respective customer."""

    start = strpdatetime(request.args.get('from'))
    end = strpdatetime(request.args.get('until'))

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
        address = get_address(_terminal(tid))

    entries = _entries(start, end, user=user, address=address)
    return JSON([entry.to_dict() for entry in entries])
