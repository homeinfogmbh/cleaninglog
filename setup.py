#! /usr/bin/env python3

from setuptools import setup


setup(
    name='cleaninglog',
    use_scm_version={
        "local_scheme": "node-and-timestamp"
    },
    setup_requires=['setuptools_scm'],
    install_requires=[
        'digsigdb',
        'flask',
        'his',
        'hwdb',
        'mdb',
        'peewee',
        'previewlib',
        'recaptcha',
        'wsgilib'
    ],
    author='HOMEINFO - Digitale Informationssysteme GmbH',
    author_email='<info@homeinfo.de>',
    maintainer='Richard Neumann',
    maintainer_email='<r.neumann@homeinfo.de>',
    packages=['cleaninglog', 'cleaninglog.wsgi'],
    license='GPLv3',
    description='HIS microservice to handle cleaning logs.'
)
