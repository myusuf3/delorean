0.6.0 (Draft)
-------------
- Makefile
    - Migrated unit tests to work with Nose and updated Makefile to run nose with the coverage plugin
- delorean/dates.py
    - partial PEP8 cleanup
    - removed unnecessary constants
    - `is_datetime_naive()` no longer returns True when dt is None
    - `localize()` works with pytz tzinfo objects
    - `normalize()` works with pytz tzinfo objects
    - `Delorean.__init__()` accepts tzinfo objects as input to timezone
    - `Delorean.timezone()` is now a property
- delorean/interface.py
    - `parse()` understands `dateutil.tz.tzoffset`, `datetutil.tz.tzlocal` and `dateutil.tz.tzutc` and converts those tzinfo
      objects into pytz based tzinfo objects.  This allows `parse()` to return a `Delorean` object with a `pytz.FixedOffset`
      timezone attached to it instead of returning a `Delorean` object converted to UTC
- tests/delorean\_tests.py
    - renamed `tests/test_data.py` to `tests/delorean_tests.py` so nose would find it and automatically run the
      unittests
- requirements.txt
    - added nose, coverage and mock as requirements for development.

