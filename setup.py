#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from version import __version__

dependencies = [
    'babel>=2.1.1',
    'humanize>=0.5.1',
    'python-dateutil>=2.4.2',
    'pytz>=2015.7',
    'tzlocal>=1.2']

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
    test_suite = 'tests.test_data',
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
