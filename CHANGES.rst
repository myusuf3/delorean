Release History
---------------

0.6.0
+++++

This release cleans up a lot of older code and makes some small modifications to the `Delorean` API to make it more
Pythonic. 0.6.0 includes support for humanizing a `Delorean` object, as well as outputing a localized string
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
