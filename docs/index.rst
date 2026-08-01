.. delorean documentation master file, created by
   sphinx-quickstart on Tue Jan  8 00:44:25 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.



Delorean: Time Travel Made Easy
================================

datetime?  Where we're going, we don't need datetime.

This document describes Delorean v\ |version|.

`Delorean` is the name of the car in the movie Back to the Future. The movie deals with a lot of time travel, hence the name Delorean as a module dealing with datetimes.

`Delorean` is a library for clearing up the inconvenient truths that arise dealing with datetimes in Python. Understanding that timing is a delicate enough of a problem `delorean` hopes to provide a cleaner less troublesome solution to shifting, manipulating, generating `datetimes`.

Delorean stands on the shoulders of giants: the standard library's `zoneinfo <https://docs.python.org/3/library/zoneinfo.html>`_ and `dateutil <https://dateutil.readthedocs.io/>`_

`Delorean` will provide natural language improvements for manipulating time, as well as datetime abstractions for ease of use. The overall goal is to improve datetime manipulations, with a little bit of software and philosophy.

Pretty much make you a badass, time traveller.

Interface Update
^^^^^^^^^^^^^^^^
Version 2.0.0 moves every timezone to the standard library. If you are coming from 1.x:

- `Delorean.timezone` now returns a `zoneinfo.ZoneInfo` or a
  `datetime.timezone`, so comparisons like ``d.timezone == pytz.utc`` need to
  become ``d.timezone == delorean.utc``.
- `delorean.timezone` and `delorean.utc` are the supported way to build a
  timezone, and `pytz` is no longer a dependency.
- A local time that happens twice, on the autumn daylight saving transition,
  now resolves to the first of its two occurrences rather than to standard
  time. Times inside the spring gap are unchanged.
- An unknown timezone name raises `DeloreanInvalidTimezone`, which is a
  `ValueError`, instead of `pytz.UnknownTimeZoneError`.
- `localize` refuses an already-aware datetime instead of silently moving the
  instant it represents.

Version 1.0.0 introduces the following breaking changes:
    - `Delorean.epoch` is a property, not a function.
    - `Delorean.midnight` is a property, not a function.
    - `Delorean.naive` is a property, not a function.
    - `Delorean.timezone` is a property, not a function.

Please make sure to update your code accordingly.

Getting Started
^^^^^^^^^^^^^^^

Here is the world without a flux capacitor at your side.::

    from datetime import datetime, timezone
    from zoneinfo import ZoneInfo

    est = ZoneInfo('US/Eastern')
    d = datetime.now(timezone.utc)
    d = d.astimezone(est)
    d

Now lets warm up the `delorean`::

    from delorean import Delorean

    d = Delorean()
    d = d.shift('US/Eastern')
    d

Look at you looking all fly. This was just a test drive checkout out what else
`delorean` can help with below.

Guide
=====

.. toctree::
    :maxdepth: 2

    license
    install
    quickstart
    interface
    contribution
    changelog
