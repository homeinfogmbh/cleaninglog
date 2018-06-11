"""Application API."""

from flask import request

from his import DATA, Application
from terminallib import Terminal
from timelib import strpdatetime
from wsgilib import JSON

from cleaninglog.messages import NoSuchTerminal, NoSuchUser
from cleaninglog.orm import User, Log
from cleaninglog.wsgi.common import get_address


APPLICATION = Application('cleaninglog', cors=True, debug=True)


def _get_terminal(cid, tid):
    """Returns the respective terminal."""

    try:
        return Terminal.by_ids(cid, tid)
    except Terminal.DoesNotExist:
        raise NoSuchTerminal()


def _get_user(pin, customer):
    """Returns the respective cleaning user."""

    try:
        return User.get(
            (User.pin == pin)
            & (User.customer == customer)
            & (User.enabled == 1))
    except User.DoesNotExist:
        return NoSuchUser()


@APPLICATION.route('/', methods=['POST'])
def add_entry():
    """Adds a cleaning entry."""

    json = DATA.json
    terminal = _get_terminal(json['cid'], json['tid'])
    user = _get_user(json['pin'], terminal.customer)
    address = get_address(terminal)
    entry = Log.add(user, address)
    entry.save()
    return ('Cleaning logged.', 201)


@APPLICATION.route('/', methods=['GET'])
def list_entries(cid, tid):
    """Lists the respective entries."""

    terminal = _get_terminal(cid, tid)
    start = strpdatetime(request.args.get('from'))
    end = strpdatetime(request.args.get('until'))
    address = get_address(terminal)
    entries = Log.slice(start, end, address=address)
    return JSON([entry.to_dict() for entry in entries])
