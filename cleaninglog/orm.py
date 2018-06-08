"""Object-relational mappings."""

from datetime import datetime

from peewee import Model, PrimaryKeyField, ForeignKeyField, CharField, \
    BooleanField, DateTimeField

from homeinfo.crm import Customer, Address
from peeweeplus import MySQLDatabase

from cleaninglog.config import CONFIG

__all__ = ['DATABASE', 'UserExists', 'User', 'Log']


DATABASE = MySQLDatabase.from_config(CONFIG['db'])


class UserExists(Exception):
    """Indicates that a respective uer already exists."""

    pass


class _CleaningVerificationModel(Model):
    """Base model for the cleaning verification database."""

    class Meta:
        database = DATABASE
        schema = DATABASE.database

    id = PrimaryKeyField()


class User(_CleaningVerificationModel):
    """A cleaning user."""

    pin = CharField(4)
    customer = ForeignKeyField(Customer, column_name='customer')
    company = CharField(64, null=True)
    enabled = BooleanField(default=True)

    @classmethod
    def add(cls, pin, customer, company=None, enabled=True):
        """Adds a user."""
        try:
            cls.get((cls.pin == pin) & (cls.customer == customer))
        except cls.DoesNotExist:
            user = cls()
            user.pin = pin
            user.customer = customer
            user.company = company
            user.enabled = enabled
            return user

        raise UserExists()

    @classmethod
    def fetch(cls, pin, customer):
        """Returns the respective user."""
        return cls.get((cls.pin == pin) & (cls.customer == customer))


class Log(_CleaningVerificationModel):
    """Actual cleaning log."""

    user = ForeignKeyField(User, column_name='user')
    address = ForeignKeyField(Address, column_name='address')
    timestamp = DateTimeField(default=datetime.now)

    @classmethod
    def add(cls, user, address, timestamp=None):
        """Adds a cleaning log entry."""
        entry = cls()
        entry.user = user
        entry.address = address
        entry.timestamp = timestamp
        return entry

    @classmethod
    def slice(cls, start, end, user=None, address=None):
        """Yields entries within the given time slice."""
        expression = True

        if start is not None:
            expression &= cls.timestamp >= start

        if end is not None:
            expression &= cls.timestamp <= end

        if user is not None:
            expression &= cls.user == user

        if address is not None:
            expression &= cls.address == address

        return cls.select().where(expression)

    def to_dict(self):
        """Returns the respective log entry as a JSON-ish dictionary."""
        return {
            'user': self.user.name,
            'address': self.address.to_dict(primary_key=False),
            'timestamp': self.timestamp.isoformat()}
