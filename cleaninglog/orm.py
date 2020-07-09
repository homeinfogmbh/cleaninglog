"""ORM models.
TODO: Curretly still located in digsigdb / alias "application".
"""
from datetime import datetime

from peewee import BooleanField, CharField, DateTimeField, ForeignKeyField

from digsigdb import DigsigdbModel
from hwdb import Deployment
from mdb import Customer

from cleaninglog import dom
from cleaninglog.exceptions import DuplicateUserError


__all__ = ['CleaningUser', 'CleaningDate', 'CleaningAnnotation']


class CleaningUser(DigsigdbModel):
    """Accounts for valet service employees."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'cleaning_user'

    name = CharField(64)
    type_ = CharField(64, column_name='type', null=True)
    customer = ForeignKeyField(Customer, column_name='customer')
    pin = CharField(4)
    annotation = CharField(255, null=True, default=None)
    created = DateTimeField()
    enabled = BooleanField(default=False)

    @classmethod
    def add(cls, name, customer, pin, annotation=None, enabled=None):
        """Adds a new cleaning user."""
        try:
            cls.get((cls.name == name) & (cls.customer == customer))
        except cls.DoesNotExist:
            record = cls()
            record.name = name
            record.customer = customer
            record.pin = pin
            record.annotation = annotation
            record.created = datetime.now()

            if enabled is not None:
                record.enabled = enabled

            record.save()
            return record

        raise DuplicateUserError()

    def to_json(self, short=False, **kwargs):
        """Returns a JSON-ish dictionary."""
        if short:
            if self.type_ is None:
                return self.name    # Compat.

            return {'name': self.name, 'type': self.type_}

        return super().to_json(**kwargs)


class CleaningDate(DigsigdbModel):
    """Cleaning chart entries."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'cleaning_date'

    user = ForeignKeyField(CleaningUser, column_name='user')
    deployment = ForeignKeyField(
        Deployment, null=True, column_name='deployment', on_delete='CASCADE',
        on_update='CASCADE')
    timestamp = DateTimeField()

    @classmethod
    def add(cls, user, deployment, annotations=None):
        """Adds a new cleaning record."""
        record = cls()
        record.user = user
        record.deployment = deployment
        record.timestamp = datetime.now()
        record.save()

        if annotations:
            for annotation in annotations:
                annotation = CleaningAnnotation(
                    cleaning_date=record, text=annotation)
                annotation.save()

        return record

    @classmethod
    def by_deployment(cls, deployment, limit=None):
        """Returns a dictionary for the respective address."""
        for counter, cleaning_date in enumerate(cls.select().where(
                cls.deployment == deployment).order_by(cls.timestamp.desc())):
            if limit is not None and counter >= limit:
                return

            yield cleaning_date

    def to_json(self, annotations=False, **kwargs):
        """Returns a JSON compliant dictionary."""
        json = super().to_json(**kwargs)

        if annotations:
            json['annotations'] = [ann.text for ann in self.annotations]

        return json

    def to_dom(self):
        """Converts the ORM model into an XML DOM."""
        xml = dom.Cleaning()
        xml.timestamp = self.timestamp
        user = dom.User(self.user.name)
        user.type = self.user.type_
        xml.user = user

        for annotation in self.annotations:
            xml.annotation.append(annotation.text)

        return xml


class CleaningAnnotation(DigsigdbModel):
    """Optional annotations for cleaning log entries."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'cleaning_annotation'

    cleaning_date = ForeignKeyField(
        CleaningDate, column_name='cleaning_date', backref='annotations',
        on_delete='CASCADE')
    text = CharField(255)
