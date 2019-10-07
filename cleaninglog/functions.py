"""Common functions."""

from flask import request

from wsgilib import ACCEPT, JSON, XML

from cleaninglog.dom import cleanings
from cleaninglog.orm import CleaningDate


__all__ = ['make_response', 'by_deployment']


def make_response(cleaning_dates):
    """Creates a response from the respective dictionary."""

    if 'application/json' in ACCEPT or '*/*' in ACCEPT:
        return JSON([
            cleaning_date.to_json(short=True)
            for cleaning_date in cleaning_dates])

    xml = cleanings()

    for cleaning_date in cleaning_dates:
        xml.cleaning.append(cleaning_date.to_dom())

    return XML(xml)


def by_deployment(deployment):
    """Returns cleaning dates of the respective deployment."""

    try:
        limit = int(request.args['limit'])
    except KeyError:
        limit = 10
    else:
        limit = limit or None

    return make_response(CleaningDate.by_deployment(deployment, limit=limit))
