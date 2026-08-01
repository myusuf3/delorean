from datetime import datetime, timezone

from dateutil.parser import isoparse as isocapture
from dateutil.parser import parse as capture
from dateutil.rrule import DAILY, HOURLY, MONTHLY, YEARLY, rrule
from dateutil.tz import tzlocal, tzoffset
from tzlocal import get_localzone

from .dates import Delorean, datetime_timezone, is_datetime_naive
from .exceptions import DeloreanInvalidDatetime
from .timezones import timezone as get_timezone
from .timezones import utc


def parse(
    datetime_str,
    timezone=None,
    isofirst=True,
    dayfirst=True,
    yearfirst=True,
    *,
    assume_timezone="UTC",
):
    """
    Parse a datetime string and return a `Delorean` object.

    :param datetime_str: The string to interpret.
    :param timezone: Force the parsed clock reading into this timezone. Any
        offset in ``datetime_str`` is discarded. To supply a timezone only
        when the string has none, use ``assume_timezone`` instead.
    :param isofirst: Try ISO parsing before the general-purpose parser.
    :param dayfirst: Interpret the first value in an ambiguous three-integer
        date (for example, ``01/05/09``) as the day rather than the month.
        When ``yearfirst`` is true, this distinguishes YDM from YMD.
    :param yearfirst: Interpret the first value in an ambiguous three-integer
        date as the year. Otherwise, interpret the last value as the year.
    :param assume_timezone: A timezone name or ``tzinfo`` object to apply when
        ``datetime_str`` contains no timezone or UTC offset. It defaults to
        ``"UTC"`` for compatibility with earlier versions. Pass ``None`` to
        assume nothing, which turns timezone-less input into an error.
    :raises DeloreanInvalidDatetime: If the string contains no timezone and
        ``assume_timezone`` is ``None``. `DeloreanInvalidDatetime` is a
        `ValueError`, as is the error raised for an unreadable string.

    .. versionadded:: 1.1.0
        The ``assume_timezone`` parameter makes the existing UTC assumption
        configurable and allows strict handling of timezone-less input.

    .. testsetup::

        from delorean import Delorean
        from delorean import parse

    .. doctest::

        >>> parse('2015-01-01 00:01:02')
        Delorean(datetime=datetime.datetime(2015, 1, 1, 0, 1, 2), timezone='UTC')

    If the string provides a fixed offset, the returned object keeps that
    offset. No assumption is necessary.

    .. doctest::

        >>> parse('2015-01-01 00:01:02 -0800')
        Delorean(datetime=datetime.datetime(2015, 1, 1, 0, 1, 2), timezone='UTC-08:00')

    A timezone-less string does not identify an instant by itself. For
    compatibility, `Delorean` assumes UTC by default. Pass a different
    ``assume_timezone`` when you know which timezone its clock reading uses.

    .. doctest::

        >>> parse('2015-01-01 00:01:02', assume_timezone='America/Toronto')
        Delorean(datetime=datetime.datetime(2015, 1, 1, 0, 1, 2), timezone='America/Toronto')

    Pass ``None`` when timezone-less input should be treated as an error rather
    than an assumed UTC value.

    .. doctest::

        >>> parse('2015-01-01 00:01:02', assume_timezone=None)  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ...
        DeloreanInvalidDatetime: ...

    ``assume_timezone`` is only a fallback. It has no effect when the string
    already includes a timezone or offset.

    .. doctest::

        >>> parse('2015-01-01 00:01:02 -0800', assume_timezone='UTC')
        Delorean(datetime=datetime.datetime(2015, 1, 1, 0, 1, 2), timezone='UTC-08:00')

    The older ``timezone`` argument is a stronger override: it discards any
    parsed offset and treats the clock reading as local to the requested
    timezone. When supplied, it takes precedence over ``assume_timezone``.

    .. doctest::

        >>> parse('2015-01-01 00:01:02 -0500', timezone='US/Pacific')
        Delorean(datetime=datetime.datetime(2015, 1, 1, 0, 1, 2), timezone='US/Pacific')

    """
    # parse string to datetime object
    dt = None
    if isofirst:
        try:
            dt = isocapture(datetime_str)
        except Exception:
            pass
    if dt is None:
        dt = capture(datetime_str, dayfirst=dayfirst, yearfirst=yearfirst)

    if timezone:
        dt = dt.replace(tzinfo=None)
        do = Delorean(datetime=dt, timezone=timezone)
    elif dt.tzinfo is None:
        if assume_timezone is None:
            raise DeloreanInvalidDatetime(
                "datetime string has no timezone and assume_timezone is None"
            )
        do = Delorean(datetime=dt, timezone=assume_timezone)
    elif isinstance(dt.tzinfo, tzoffset):
        tz = get_timezone(dt.tzinfo)
        dt = dt.replace(tzinfo=None)
        do = Delorean(dt, timezone=tz)
    elif isinstance(dt.tzinfo, tzlocal):
        tz = get_localzone()
        dt = dt.replace(tzinfo=None)
        do = Delorean(dt, timezone=tz)
    else:
        dt = dt.astimezone(utc)
        # making dt naive so we can pass it to Delorean
        dt = dt.replace(tzinfo=None)
        # if parse string has tzinfo we return a normalized UTC
        # delorean object that represents the time.
        do = Delorean(datetime=dt, timezone=utc)

    return do


def range_daily(start=None, stop=None, timezone="UTC", count=None):
    """
    This an alternative way to generating sets of Delorean objects with
    DAILY stops
    """
    return stops(start=start, stop=stop, freq=DAILY, timezone=timezone, count=count)


def range_hourly(start=None, stop=None, timezone="UTC", count=None):
    """
    This an alternative way to generating sets of Delorean objects with
    HOURLY stops
    """
    return stops(start=start, stop=stop, freq=HOURLY, timezone=timezone, count=count)


def range_monthly(start=None, stop=None, timezone="UTC", count=None):
    """
    This an alternative way to generating sets of Delorean objects with
    MONTHLY stops
    """
    return stops(start=start, stop=stop, freq=MONTHLY, timezone=timezone, count=count)


def range_yearly(start=None, stop=None, timezone="UTC", count=None):
    """
    This an alternative way to generating sets of Delorean objects with
    YEARLY stops
    """
    return stops(start=start, stop=stop, freq=YEARLY, timezone=timezone, count=count)


def stops(
    freq,
    interval=1,
    count=None,
    wkst=None,
    bysetpos=None,
    bymonth=None,
    bymonthday=None,
    byyearday=None,
    byeaster=None,
    byweekno=None,
    byweekday=None,
    byhour=None,
    byminute=None,
    bysecond=None,
    timezone="UTC",
    start=None,
    stop=None,
):
    """
    Yield a Delorean object for each stop matching the settings passed in.
    """
    # check to see if datetimes passed in are naive if so process them
    # with given timezone.
    if all(
        [
            (start is None or is_datetime_naive(start)),
            (stop is None or is_datetime_naive(stop)),
        ]
    ):
        pass
    else:
        raise DeloreanInvalidDatetime("Provide a naive datetime object")

    # if no datetimes are passed in create a proper datetime object for
    # start default because default in dateutil is datetime.now() :(
    if start is None:
        start = datetime_timezone(timezone)

    for dt in rrule(
        freq,
        interval=interval,
        count=count,
        wkst=wkst,
        bysetpos=bysetpos,
        bymonth=bymonth,
        bymonthday=bymonthday,
        byyearday=byyearday,
        byeaster=byeaster,
        byweekno=byweekno,
        byweekday=byweekday,
        byhour=byhour,
        byminute=byminute,
        bysecond=bysecond,
        until=stop,
        dtstart=start,
    ):
        # make the delorean object
        # yield it.
        # doing this to make sure delorean receives a naive datetime.
        dt = dt.replace(tzinfo=None)
        d = Delorean(datetime=dt, timezone=timezone)
        yield d


def from_timestamp(s):
    """
    Return a `Delorean` object for the given seconds since the Unix epoch.

    .. testsetup::

        from delorean import from_timestamp

    .. doctest::

        >>> from_timestamp(1420099200.0)
        Delorean(datetime=datetime.datetime(2015, 1, 1, 8, 0), timezone='UTC')

    """
    dt = datetime.fromtimestamp(s, timezone.utc).replace(tzinfo=None)
    return Delorean(datetime=dt, timezone="UTC")


def epoch(s):
    """
    Alias of :func:`from_timestamp`, kept for backwards compatibility.

    The argument is seconds since the Unix epoch rather than an epoch, so
    `from_timestamp` is the more accurate name. It also avoids `epoch`
    meaning two opposite things, since :attr:`Delorean.epoch` converts the
    other way.
    """
    return from_timestamp(s)


def flux():
    print("If you put your mind to it, you can accomplish anything.")


def utcnow():
    """
    Return a Delorean object for the current UTC date and time, setting the timezone to UTC.
    """
    return Delorean()


def now(timezone=None):
    """
    Return a Delorean object for the current local date and time, setting the timezone to the local timezone of the
    caller by default.

    :param Optional[datetime.tzinfo] timezone: A custom timezone to use when computing the time.
    :rtype: delorean.dates.Delorean
    """
    return Delorean(timezone=timezone or get_localzone())
