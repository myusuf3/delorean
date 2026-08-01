"""
Timezone objects for delorean's public API.

Every timezone delorean hands back is a standard library object: a
`zoneinfo.ZoneInfo` for a named zone, or a `datetime.timezone` for a fixed
offset. `timezone` is the only constructor a caller needs, so working with
`Delorean` objects never means importing a timezone library of your own.
"""

import re
from datetime import timedelta, tzinfo
from datetime import timezone as fixed_offset
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from dateutil.tz import tzoffset

from .exceptions import DeloreanInvalidTimezone

utc = ZoneInfo("UTC")

# `str(datetime.timezone(...))` renders a fixed offset in this form, which is
# what `Delorean.__repr__` prints, so repr output round-trips back through
# `timezone()`.
_OFFSET = re.compile(r"^UTC([+-])(\d{2}):(\d{2})(?::(\d{2}))?$")


def timezone(name):
    """
    Return the timezone that `name` identifies.

    :param name: An IANA zone name such as ``"US/Eastern"``, a fixed offset
        written as ``"UTC-08:00"``, or a `tzinfo` object, which is returned
        unchanged so this can normalize whatever a caller supplies.
    :raises DeloreanInvalidTimezone: If the name identifies no known zone.

    .. testsetup::

        from delorean import timezone

    .. doctest::

        >>> timezone('US/Eastern')
        zoneinfo.ZoneInfo(key='US/Eastern')
        >>> timezone('UTC-08:00')
        datetime.timezone(datetime.timedelta(days=-1, seconds=57600))

    .. versionadded:: 2.0

    """
    if isinstance(name, tzoffset):
        # dateutil's offsets reach here from parsed strings; convert them so
        # every fixed offset delorean stores is the same type.
        return fixed_offset(name.utcoffset(None))

    if isinstance(name, tzinfo):
        return name

    match = _OFFSET.match(name) if isinstance(name, str) else None
    if match:
        sign, hours, minutes, seconds = match.groups()
        offset = timedelta(
            hours=int(hours), minutes=int(minutes), seconds=int(seconds or 0)
        )
        return fixed_offset(-offset if sign == "-" else offset)

    try:
        return ZoneInfo(name)
    except (ZoneInfoNotFoundError, ValueError, TypeError):
        raise DeloreanInvalidTimezone(f"Unknown timezone: {name!r}") from None
