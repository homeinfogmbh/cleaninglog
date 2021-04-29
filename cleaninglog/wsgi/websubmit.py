"""Web interface to submit cleaning log entries."""

from datetime import datetime
from typing import Union

from flask import request

from hwdb import Deployment
from recaptcha import verify
from wsgilib import Application, Error, OK

from cleaninglog.orm import CleaningDate, CleaningUser


__all__ = ['APPLICATION']


CORS = {'origins': 'cleaninglog.homeinfo.de'}
APPLICATION = Application('cleaninglog', cors=CORS)
RECAPTCHA_SECRET = ''


def authorize(deployment_id: int, pin: str) -> Deployment:
    """Returns the respective cleaning user and deployment if
    the user identified by the PIN may submit entries for it.
    """

    deployment = Deployment.select(cascade=True).where(
        Deployment.id == deployment_id).get()
    cleaning_user = CleaningUser.select().where(
        (CleaningUser.customer == deployment.customer)
        & (CleaningUser.pin == pin)
        & (CleaningUser.created < datetime.now())
        & (CleaningUser.enabled == 1)
    ).get()
    return (cleaning_user, deployment)


@APPLICATION.route('/', methods=['POST'])
def submit() -> Union[Error, OK]:
    """Submits an entry."""

    recaptcha_response = request.json.pop('recaptcha_response')

    if not verify(RECAPTCHA_SECRET, recaptcha_response, fail_silently=True):
        return Error('ReCAPTCHA check failed.', status=403)

    deployment_id = request.json.pop('deployment')
    pin = request.json.pop('pin')

    try:
        cleaning_user, deployment = authorize(deployment_id, pin)
    except (Deployment.DoesNotExist, CleaningUser.DoesNotExist):
        return Error('Invalid credentials.', status=403)

    annotations = request.json.pop('annotations')
    CleaningDate.add(cleaning_user, deployment, annotations)
    return OK('Cleaning date added.')
