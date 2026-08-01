Release History
---------------

2.0.0
+++++

Breaking changes
~~~~~~~~~~~~~~~~

- Timezones are now standard library objects. ``Delorean.timezone`` returns a
  ``zoneinfo.ZoneInfo`` for a named zone or a ``datetime.timezone`` for a fixed
  offset, and ``pytz`` is no longer a dependency. Comparisons such as
  ``d.timezone == pytz.utc`` become ``d.timezone == delorean.utc``. (#79)
- ``midnight``, ``start_of_day`` and ``end_of_day`` return ``Delorean`` objects
  rather than bare ``datetime`` objects, so they compose with the shift methods.
  Callers doing ``d.midnight.strftime(...)`` need ``d.midnight.datetime``. (#139)
- A local time that occurs twice, on the autumn daylight saving transition, now
  resolves to the first of its two occurrences, following the standard library's
  ``fold=0``. Earlier versions resolved it to standard time via pytz's
  ``is_dst=False``. Times inside the spring-forward gap are unchanged.
- An unknown timezone name raises ``DeloreanInvalidTimezone``, which is a
  ``ValueError``, instead of ``pytz.UnknownTimeZoneError``.
- ``localize()`` rejects an already-aware datetime instead of silently replacing
  its timezone, which moved the instant the value represented.
- ``repr()`` prints a fixed offset as ``'UTC-08:00'`` rather than
  ``pytz.FixedOffset(-480)``. The constructor accepts that string, so repr output
  still round-trips through ``eval()``.


Added
~~~~~

- ``parse()`` takes a keyword-only ``assume_timezone``, which controls the
  timezone applied to a string that carries none. It defaults to ``"UTC"``,
  matching earlier behaviour, and accepts ``None`` to reject such input instead. (#53)
- ``delorean.timezone()`` and ``delorean.utc``, so callers never import a
  timezone library of their own. ``timezone()`` accepts an IANA name, a fixed
  offset written as ``"UTC-08:00"``, or an existing ``tzinfo`` object. (#79)
- ``start_of_month``, ``end_of_month``, ``start_of_year`` and ``end_of_year``. (#85)
- ``Delorean.timestamp`` and ``from_timestamp()``, naming the value for what it
  is. ``epoch`` remains as an alias. (#86)


Changed
~~~~~~~

- Note for upgraders: ``delorean.dates.UTC``, an undocumented constant equal to
  the string ``"UTC"``, was removed back in 0.6.0. Use ``"UTC"`` or
  ``delorean.utc``. (#95)
- Packaging moved to ``pyproject.toml`` with hatchling, and the version is
  single-sourced there. Documentation gained executed examples throughout,
  covering daylight saving resolution and month-end clamping (#11).
- ``DeloreanError`` subclasses ``ValueError``, so one ``except ValueError``
  covers both delorean's errors and the parser's error for unreadable input. It
  is also exported from the package root.


Fixed
~~~~~

- Fractional second shifts no longer truncate to zero. ``next_second(0.5)`` moves
  half a second, and calendar units reject non-integer counts with a
  ``TypeError`` rather than silently doing nothing. (#75)
- ISO 8601 strings parse correctly. This fix has been on master since 2018 and
  reaches a release for the first time here. (#103)
- ``Delorean.__getattr__`` returned the ``AttributeError`` class instead of
  raising it, so ``hasattr()`` reported ``True`` for invalid shift names.
- ``now()`` raised ``AttributeError`` under tzlocal 5.x, which returns a
  ``zoneinfo`` zone where delorean called pytz-only methods. ``normalize()`` hit
  the same fault for any datetime delorean had itself localized.


Removed
~~~~~~~

- Python 3.9 is no longer supported; ``requires-python`` is now ``>=3.10``.


1.0.0
+++++

This release cleans up a lot of older code and makes some small modifications to the `Delorean` API to make it more
Pythonic. 1.0.0 includes support for humanizing a `Delorean` object, as well as outputing a localized string
representing the `Delorean` object.

This change introduces the following breaking changes:
    - `Delorean.epoch` is a property, not a function.
    - `Delorean.midnight` is a property, not a function.
    - `Delorean.naive` is a property, not a function.
    - `Delorean.timezone` is a property, not a function.

- delorean/dates.py
    - `is_datetime_naive()` no longer returns True when dt is None
    - `localize()` works with pytz tzinfo objects
    - `normalize()` works with pytz tzinfo objects
    - `Delorean.__init__()` accepts tzinfo objects as input to timezone
    - `Delorean.timezone()` is now a property
    - Added suport for humanizing a `Delorean` object
    - Added support for localizing a `Delorean` object for string output
- delorean/interface.py
    - `parse()` understands `dateutil.tz.tzoffset`, `datetutil.tz.tzlocal` and `dateutil.tz.tzutc` and converts those tzinfo
      objects into pytz based tzinfo objects.  This allows `parse()` to return a `Delorean` object with a `pytz.FixedOffset`
      timezone attached to it instead of returning a `Delorean` object converted to UTC
