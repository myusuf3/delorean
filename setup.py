#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from version import __version__

dependencies = [
    'babel>=2.10.3',
    'humanize>=4.2.2',
    'python-dateutil>=2.8.2',
    'pytz>=2022.1',
    'tzlocal>=4.2']

setup(
    name='Delorean',
    version='.'.join(str(x) for x in __version__),
    description='library for manipulating datetimes with ease and clarity',
    url='https://github.com/myusuf3/delorean',
    author='Mahdi Yusuf',
    author_email="yusuf.mahdi@gmail.com",
    packages=['delorean'],
    license='MIT license',
    install_requires=dependencies,
    test_suite='tests.test_data',
    long_description=open('README.rst').read(),
    python_requires='>=3.0, !=3.0.*',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
