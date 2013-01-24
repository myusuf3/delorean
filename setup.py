#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from version import __version__

dependencies = ['pytz>=2012h', 'python-dateutil==2.1']

setup(
    name='Delorean',
    version='.'.join(str(x) for x in __version__),
    description='library for manipulating datetimes with ease and clarity',
    url='https://github.com/myusuf3/delorean',
    author='Mahdi Yusuf',
    author_email="yusuf.mahdi@gmail.com",
    packages=[
    'delorean',
    ],
    license='MIT license',
    install_requires=dependencies,
    long_description=open('README.rst').read(),
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ),
)
