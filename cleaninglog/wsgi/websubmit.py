"""Web interface to submit cleaning log entries."""

from configparser import ConfigParser
from datetime import datetime
from pathlib import Path
from typing import Union

from flask import request

from hwdb import Deployment
from recaptcha import verify
from wsgilib import Application, Error, OK

from cleaninglog.orm import CleaningDate, CleaningUser


__all__ = ['APPLICATION']


CORS = {'origins': ['https://cleaninglog.homeinfo.de']}
APPLICATION = Application('cleaninglog', cors=CORS)
CONFIG = ConfigParser()
CONFIG_FILE = Path('/usr/local/etc/cleaninglog.conf')
CONFIG.read(CONFIG_FILE)


def authorize(deployment_id: int, pin: str) -> tuple[CleaningUser, Deployment]:
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
    return cleaning_user, deployment


@APPLICATION.route('/', methods=['POST'], strict_slashes=False)
def submit() -> Union[Error, OK]:
    """Submits an entry."""

    recaptcha_secret = CONFIG.get('recaptcha', 'secret')
    recaptcha_response = request.json.pop('recaptchaResponse')

    if not verify(recaptcha_secret, recaptcha_response, fail_silently=True):
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
