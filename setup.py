#! /usr/bin/env python3

from distutils.core import setup


setup(
    name='cleaninglog',
    version='latest',
    author='HOMEINFO - Digitale Informationssysteme GmbH',
    author_email='<info at homeinfo dot de>',
    maintainer='Richard Neumann',
    maintainer_email='<r dot neumann at homeinfo priod de>',
    packages=['cleaninglog', 'cleaninglog.wsgi'],
    data_files=[('/etc/his.d/locale', ['files/cleaninglog.ini'])],
    license='GPLv3',
    description='HIS microservice to handle cleaning logs.')
