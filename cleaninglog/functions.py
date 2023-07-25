"""Common functions."""

from typing import Iterable, Union

from flask import request

from hwdb import Deployment
from wsgilib import ACCEPT, JSON, XML

from cleaninglog.dom import cleanings
from cleaninglog.orm import CleaningDate


__all__ = ["make_response", "by_deployment"]


def make_response(cleaning_dates: Iterable[CleaningDate]) -> Union[JSON, XML]:
    """Creates a response from the respective dictionary."""

    if "application/json" in ACCEPT:
        return JSON([cd.to_json() for cd in cleaning_dates])

    xml = cleanings()

    for cleaning_date in cleaning_dates:
        xml.cleaning.append(cleaning_date.to_dom())

    return XML(xml)


def by_deployment(deployment: Deployment) -> Union[JSON, XML]:
    """Returns cleaning dates of the respective deployment."""

    try:
        limit = int(request.args["limit"])
    except KeyError:
        limit = 10
    else:
        limit = limit or None

    return make_response(CleaningDate.by_deployment(deployment, limit=limit))
