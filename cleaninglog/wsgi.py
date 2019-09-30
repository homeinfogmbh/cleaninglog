"""Authenticated and authorized HIS services."""

from datetime import datetime

from flask import request

from digsigdb import CleaningUser, CleaningDate, CleaningAnnotation
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


def _get_users():
    """Yields the customer's users."""

    return CleaningUser.select().where(
        (CleaningUser.customer == CUSTOMER.id) & _cleaning_user_selects())


def _get_user(ident):
    """Returns the respective user."""

    try:
        return CleaningUser.get(
            (CleaningUser.id == ident)
            & (CleaningUser.customer == CUSTOMER.id)
            & _cleaning_user_selects()
        )
    except CleaningUser.DoesNotExist:
        raise NO_SUCH_USER


def _get_deployment(ident):
    """Returns a deployment by its id."""

    try:
        return Deployment.get(
            (Deployment.id == ident)
            & (Deployment.customer == CUSTOMER.id)
        )
    except Deployment.DoesNotExist:
        return NO_SUCH_DEPLOYMENT


def _get_system(ident):
    """Returns the respective system."""

    try:
        return System.select().join(Deployment).where(
            (System.id == ident)
            & (Deployment.customer == CUSTOMER.id)
        ).get()
    except System.DoesNotExist:
        raise NO_SUCH_SYSTEM


def _address_of(system):
    """Returns the system's address."""

    deployment = system.deployment

    if deployment is None:
        return SYSTEM_NOT_DEPLOYED

    return deployment.address


def _get_entries(since, until, user=None, deployment=None):
    """Yields the respective customer's entries."""

    if user is None:
        expression = CleaningDate.user << {user.id for user in _get_users()}
    else:
        expression = CleaningDate.user == user

    if deployment is not None:
        expression &= CleaningDate.deployment == deployment

    if since is not None:
        expression &= CleaningDate.timestamp >= since

    if until is not None:
        expression &= CleaningDate.timestamp <= until

    return CleaningDate.select().where(expression)


@authenticated
@authorized('cleaninglog')
def list_users():
    """Lists the cleaning log users of the respective customer."""

    return JSON([user.to_json() for user in _get_users()])


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
    else:
        user = _get_user(user)

    try:
        deployment = request.args['deployment']
    except KeyError:
        deployment = None
    else:
        deployment = _get_deployment(deployment)

    entries = _get_entries(since, until, user=user, deployment=deployment)
    entries = [entry.to_json(annotations=True, cascade=3) for entry in entries]
    return JSON(entries)


@authenticated
@authorized('cleaninglog')
def add_entry():
    """Adds a cleaning log entry."""

    try:
        user = request.json.pop('user')
    except KeyError:
        return NO_USER_SPECIFIED

    user = _get_user(user)

    try:
        deployment = request.json.pop('deployment')
    except KeyError:
        return NO_DEPLOYMENT_SPECIFIED

    deployment = _get_deployment(deployment)
    annotations = request.json.pop('annotations', None)
    record = CleaningDate.from_json(request.json)
    record.user = user
    record.deployment = deployment
    record.save()

    if annotations:
        for text in annotations:
            CleaningAnnotation(cleaning_date=record, text=text).save()

    return ENTRY_CREATED.update(id=record.id)


APPLICATION.add_routes((
    ('GET', '/', list_entries, 'list_entries'),
    ('GET', '/users', list_users, 'list_users')
))
