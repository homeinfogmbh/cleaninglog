"""Application API."""

from his import DATA, Application
from terminallib import Terminal
from timelib import strpdatetime
from wsgilib import Error

from cleaninglog.orm import User, Log


APPLICATION = Application('cleaninglog', cors=True, debug=True)


def _get_terminal(cid, tid):
    """Returns the respective terminal."""

    try:
        return Terminal.by_ids(cid, tid)
    except Terminal.DoesNotExist:
        raise Error('No such terminal.', status=404)


def _get_user(pin, customer):
    """Returns the respective cleaning user."""

    try:
        return User.get(
            (User.pin == pin)
            & (User.customer == customer)
            & (User.enabled == 1))
    except User.DoesNotExist:
        return ('No such user.', 404)


def _get_address(terminal):
    """Returns the terminal's address."""

    try:
        return terminal.location.address
    except AttributeError:
        return ('Terminal has no address.', 420)


def add_entry():
    """Adds a cleaning entry."""

    json = DATA.json
    terminal = _get_terminal(json['cid'], json['tid'])
    user = _get_user(json['pin'], terminal.customer)
    address = _get_address(terminal)
    entry = Log.add(user, address)
    entry.save()
    return ('Cleaning logged.', 201)


def list_entries(cid, tid):
    """Lists the respective entries."""

    terminal = _get_terminal(cid, tid)
    from_ = strpdatetime(request.args.get('from'))
    until = strpdatetime(request.args.get('until'))
    address = _get_address(terminal)
    entries = Log.slice(from_, until, address=address)
    return JSON([entry.to_dict() for entry in entries])
