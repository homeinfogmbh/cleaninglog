"""Common functions."""

from wsgilib import ACCEPT, JSON, XML

from cleaninglog.dom import cleanings


__all__ = ['make_response']


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
