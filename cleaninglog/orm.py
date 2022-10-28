"""ORM models.
TODO: Currently still located in digsigdb / alias "application".
"""
from __future__ import annotations
from datetime import datetime
from typing import Iterable, Iterator, Optional

from peewee import BooleanField
from peewee import CharField
from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import ModelSelect

from digsigdb import DigsigdbModel
from hwdb import Deployment
from mdb import Address, Company, Customer

from cleaninglog import dom
from cleaninglog.exceptions import DuplicateUserError


__all__ = ['CleaningUser', 'CleaningDate', 'CleaningAnnotation']


class CleaningUser(DigsigdbModel):
    """Accounts for valet service employees."""

    class Meta:
        table_name = 'cleaning_user'

    name = CharField(64)
    type = CharField(64, null=True)
    customer = ForeignKeyField(
        Customer, column_name='customer', on_delete='CASCADE', lazy_load=False
    )
    pin = CharField(4)
    annotation = CharField(255, null=True, default=None)
    created = DateTimeField(datetime.now)
    enabled = BooleanField(default=False)

    @classmethod
    def add(
            cls,
            name: str,
            customer: Customer,
            pin: str,
            annotation: str = None,
            enabled: bool = None
    ) -> CleaningUser:
        """Adds a new cleaning user."""
        try:
            cls.get((cls.name == name) & (cls.customer == customer))
        except cls.DoesNotExist:
            record = cls(
                name=name,
                customer=customer,
                pin=pin,
                annotation=annotation
            )

            if enabled is not None:
                record.enabled = enabled

            record.save()
            return record

        raise DuplicateUserError()

    @classmethod
    def select(cls, *args, cascade: bool = False) -> ModelSelect:
        """Selects cleaning users."""
        if not cascade:
            return super().select(*args)

        return super().select(
            cls, Customer, Company, *args
        ).join(Customer).join(Company)

    def to_json(self, short: bool = False, **kwargs) -> dict:
        """Returns a JSON-ish dictionary."""
        if short:
            if self.type is None:
                return self.name    # Compat.

            return {'name': self.name, 'type': self.type}

        return super().to_json(**kwargs)

    def to_dom(self) -> dom.User:
        """Converts the ORM model into an XML DOM."""
        return dom.User(self.name, type=self.type)


class CleaningDate(DigsigdbModel):
    """Cleaning chart entries."""

    class Meta:
        table_name = 'cleaning_date'

    user = ForeignKeyField(
        CleaningUser, column_name='user', on_delete='CASCADE', lazy_load=False
    )
    deployment = ForeignKeyField(
        Deployment, null=True, column_name='deployment', on_delete='CASCADE',
        on_update='CASCADE', lazy_load=False
    )
    timestamp = DateTimeField(default=datetime.now)
    user_timestamp = DateTimeField(null=True)

    @classmethod
    def add(
            cls,
            user: CleaningUser,
            deployment: Deployment,
            annotations: Iterable[str] = (),
            user_timestamp: Optional[datetime] = None
    ) -> CleaningDate:
        """Adds a new cleaning record."""
        record = cls(
            user=user,
            deployment=deployment,
            user_timestamp=user_timestamp
        )
        record.save()

        for annotation in annotations:
            annotation = CleaningAnnotation(
                cleaning_date=record, text=annotation
            )
            annotation.save()

        return record

    @classmethod
    def by_deployment(
            cls,
            deployment: Deployment,
            limit: bool = None
    ) -> Iterator[CleaningDate]:
        """Returns a dictionary for the respective address."""
        for counter, cleaning_date in enumerate(
                cls.select(cascade=True).where(
                    cls.deployment == deployment).order_by(
                    cls.timestamp.desc())
        ):
            if limit is not None and counter >= limit:
                return

            yield cleaning_date

    @classmethod
    def select(cls, *args, cascade: bool = False) -> ModelSelect:
        """Selects cleaning dates."""
        if not cascade:
            return super().select(*args)

        deployment_address = Address.alias()
        return super().select(
            cls, CleaningUser, Customer, Company, Deployment,
            deployment_address, *args
        ).join(CleaningUser).join(
            Customer).join(Company).join_from(cls, Deployment).join(
            deployment_address, on=Deployment.address == deployment_address.id
        )

    def to_json(self, **kwargs) -> dict:
        """Returns a JSON compliant dictionary."""
        json = super().to_json(**kwargs)
        json['user'] = self.user.to_json(short=True)
        json['annotations'] = [ann.text for ann in self.annotations]
        return json

    def to_dom(self) -> dom.Cleaning:
        """Converts the ORM model into an XML DOM."""
        xml = dom.Cleaning()
        xml.timestamp = self.timestamp
        xml.user = self.user.to_dom()

        for annotation in self.annotations:
            xml.annotation.append(annotation.text)

        return xml


class CleaningAnnotation(DigsigdbModel):
    """Optional annotations for cleaning log entries."""

    class Meta:
        table_name = 'cleaning_annotation'

    cleaning_date = ForeignKeyField(
        CleaningDate, column_name='cleaning_date', backref='annotations',
        on_delete='CASCADE'
    )
    text = CharField(255)
