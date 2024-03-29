"""Authenticated and authorized HIS services."""

from datetime import datetime
from typing import Iterable

from flask import request
from peewee import Expression

from his import CUSTOMER, authenticated, authorized, Application
from hwdb import Deployment, System
from previewlib import preview, DeploymentPreviewToken
from wsgilib import JSON, JSONMessage

from cleaninglog.functions import by_deployment
from cleaninglog.messages import CLEANING_DATE_CREATED
from cleaninglog.messages import CLEANING_DATE_DELETED
from cleaninglog.messages import CLEANING_DATE_PATCHED
from cleaninglog.messages import NO_DEPLOYMENT_SPECIFIED
from cleaninglog.messages import NO_SUCH_CLEANING_DATE
from cleaninglog.messages import NO_SUCH_DEPLOYMENT
from cleaninglog.messages import NO_SUCH_SYSTEM
from cleaninglog.messages import NO_SUCH_USER
from cleaninglog.messages import NO_USER_SPECIFIED
from cleaninglog.orm import CleaningUser, CleaningDate, CleaningAnnotation


__all__ = ["APPLICATION"]


APPLICATION = Application("Cleaning Log", debug=True)


def _cleaning_user_selects() -> Expression:
    """Returns a basic expression for cleaning users selection."""

    return (CleaningUser.created < datetime.now()) & (CleaningUser.enabled == 1)


def _get_users() -> Iterable[CleaningUser]:
    """Yields the customer's users."""

    return CleaningUser.select(cascade=True).where(
        (CleaningUser.customer == CUSTOMER.id) & _cleaning_user_selects()
    )


def _get_user(ident: int) -> CleaningUser:
    """Returns the respective user."""

    try:
        return (
            CleaningUser.select(cascade=True)
            .where(
                (CleaningUser.id == ident)
                & (CleaningUser.customer == CUSTOMER.id)
                & _cleaning_user_selects()
            )
            .get()
        )
    except CleaningUser.DoesNotExist:
        raise NO_SUCH_USER from None


def _get_deployment(ident: int) -> Deployment:
    """Returns a deployment by its id."""

    try:
        return (
            Deployment.select(cascade=True)
            .where((Deployment.id == ident) & (Deployment.customer == CUSTOMER.id))
            .get()
        )
    except Deployment.DoesNotExist:
        raise NO_SUCH_DEPLOYMENT from None


def _get_system(ident: int) -> System:
    """Returns the respective system."""

    condition = (System.id == ident) & (Deployment.customer == CUSTOMER.id)

    try:
        return System.select(cascade=True).where(condition).get()
    except System.DoesNotExist:
        raise NO_SUCH_SYSTEM from None


def _get_entries(
    since: datetime,
    until: datetime,
    users: Iterable[CleaningUser] = None,
    deployment: Deployment = None,
) -> Iterable[CleaningDate]:
    """Yields the respective customer's entries."""

    if users is None:
        users = {user.id for user in _get_users()}

    expression = CleaningDate.user << users

    if deployment is not None:
        expression &= CleaningDate.deployment == deployment

    if since is not None:
        expression &= CleaningDate.timestamp >= since

    if until is not None:
        expression &= CleaningDate.timestamp <= until

    return CleaningDate.select(cascade=True).where(expression)


def _get_cleaning_date(ident: int) -> CleaningDate:
    """Returns the respective cleaning date."""

    try:
        return (
            CleaningDate.select(cascade=True)
            .where((CleaningDate.id == ident) & (CleaningUser.customer == CUSTOMER.id))
            .get()
        )
    except CleaningDate.DoesNotExist:
        raise NO_SUCH_CLEANING_DATE from None


@authenticated
@authorized("cleaninglog")
def list_users() -> JSON:
    """Lists the cleaning log users of the respective customer."""

    return JSON([user.to_json() for user in _get_users()])


@authenticated
@authorized("cleaninglog")
def list_entries() -> JSON:
    """Lists the cleaning log entries of the respective customer."""

    if (since := request.args.get("since")) is not None:
        since = datetime.fromisoformat(since)

    if (until := request.args.get("until")) is not None:
        until = datetime.fromisoformat(until)

    try:
        user = int(request.args["user"])
    except KeyError:
        users = None
    else:
        users = {_get_user(user)}

    try:
        deployment = request.args["deployment"]
    except KeyError:
        deployment = None
    else:
        deployment = _get_deployment(int(deployment))

    entries = _get_entries(since, until, users=users, deployment=deployment)
    entries = [entry.to_json(cascade=3) for entry in entries]
    return JSON(entries)


@authenticated
@authorized("cleaninglog")
def add_entry() -> JSONMessage:
    """Adds a cleaning log entry."""

    try:
        user = request.json.pop("user")
    except KeyError:
        return NO_USER_SPECIFIED

    user = _get_user(user)

    try:
        deployment = request.json.pop("deployment")
    except KeyError:
        return NO_DEPLOYMENT_SPECIFIED

    deployment = _get_deployment(deployment)
    annotations = request.json.pop("annotations", None)
    cleaning_date = CleaningDate.from_json(request.json)
    cleaning_date.user = user
    cleaning_date.deployment = deployment
    cleaning_date.save()

    for text in annotations or ():
        CleaningAnnotation(cleaning_date=cleaning_date, text=text).save()

    return CLEANING_DATE_CREATED.update(id=cleaning_date.id)


@authenticated
@authorized("cleaninglog")
def modify_entry(ident: int) -> JSONMessage:
    """Modifies a cleaning log entry."""

    cleaning_date = _get_cleaning_date(ident)

    try:
        user = request.json.pop("user")
    except KeyError:
        pass
    else:
        cleaning_date.user = _get_user(user)

    try:
        deployment = request.json.pop("deployment")
    except KeyError:
        pass
    else:
        cleaning_date.deployment = _get_deployment(deployment)

    try:
        annotations = request.json.pop("annotations")
    except KeyError:
        pass
    else:
        for annotation in cleaning_date.annotations:
            annotation.delete_instance()

        for text in annotations or ():
            CleaningAnnotation(cleaning_date=cleaning_date, text=text).save()

    cleaning_date.patch_json(request.json)
    cleaning_date.save()
    return CLEANING_DATE_PATCHED


@authenticated
@authorized("cleaninglog")
def delete_entry(ident: int) -> JSONMessage:
    """Deletes a cleaning log entry."""

    cleaning_date = _get_cleaning_date(ident)
    cleaning_date.delete_instance()
    return CLEANING_DATE_DELETED


APPLICATION.add_routes(
    [
        ("GET", "/users", list_users),
        ("GET", "/", list_entries),
        ("POST", "/", add_entry),
        ("PATCH", "/<int:ident>", modify_entry),
        ("DELETE", "/<int:ident>", delete_entry),
        ("GET", "/preview", preview(DeploymentPreviewToken)(by_deployment)),
    ]
)
