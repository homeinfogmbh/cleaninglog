"""WSGI services."""

from cleaninglog.wsgi.application import APPLICATION
from cleaninglog.wsgi.his import APPLICATION as HIS

__all__ = ['APPLICATION', 'HIS']
