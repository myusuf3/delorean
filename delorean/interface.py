from datetime import datetime

from pytz import timezone
from dateutil.rrule import rrule, DAILY, HOURLY, MONTHLY, YEARLY
from dateutil.parser import parse as capture

from .exceptions import DeloreanInvalidDatetime
from .dates import Delorean, is_datetime_naive, datetime_timezone

UTC = "UTC"
utc = timezone("utc")

NAIVEMODE_UTC = "utc"
NAIVEMODE_NAIVE = "naive"
NAIVEMODE_RAISE = "raise"
NAIVE_MODES = (NAIVEMODE_UTC, NAIVEMODE_NAIVE, NAIVEMODE_RAISE)

def parse(s, dayfirst=True, yearfirst=True, naivemode=NAIVEMODE_UTC):
    """
    Parses a datetime string in it and returns a `Delorean` object.

    If a timezone is detected in the datetime string it will be
    normalized to UTC, and a Delorean object with that datetime and
    timezone will be returned.

    If a timezone is not detected, the resulting timezone (and return object)
    depends on the value of the naivemode argument:
        '{mode_utc}' -- UTC is assumed
        '{mode_raise}' -- An exception is raised
        '{mode_naive}' -- Returns a naive datetime object (NOT a `Delorean`).

    Note that in the case of naivemode=='{mode_naive}' a Delorean object is
    not returned. This is because Delorean objects should always be timezone
    aware.

    """

    if not naivemode in NAIVE_MODES:
        raise ValueError("Unknown naivemode value: '%s'" % naivemode)

    try:
        dt = capture(s, dayfirst=dayfirst, yearfirst=yearfirst)
    except:
        # raise a parsing error.
        raise ValueError("Unknown string format")
    if dt.tzinfo is None:
        if naivemode == NAIVEMODE_UTC:
            # assuming datetime object passed in is UTC
            do = Delorean(datetime=dt, timezone=UTC)
        elif naivemode == NAIVEMODE_RAISE:
            raise DeloreanInvalidDatetime("Unable to determine timezone info")
        elif naivemode == NAIVEMODE_NAIVE:
            do = dt #note that we are *not* returning a Delorean here
    else:
        dt = utc.normalize(dt)
        # makeing dt naive so we can pass it to Delorean
        dt = dt.replace(tzinfo=None)
        # if parse string has tzinfo we return a normalized UTC
        # delorean object that represents the time.
        do = Delorean(datetime=dt, timezone=UTC)
    return do
try:
    parse.__doc__ = parse.__doc__.format(mode_utc=NAIVEMODE_UTC,
                                         mode_raise=NAIVEMODE_RAISE,
                                         mode_naive=NAIVEMODE_NAIVE)
except AttributeError:
    #must be running with -OO
    pass

def range_daily(start=None, stop=None, timezone=UTC, count=None):
    """
    This an alternative way to generating sets of Delorean objects with
    DAILY stops
    """
    return stops(start=start, stop=stop, freq=DAILY, timezone=timezone, count=count)


def range_hourly(start=None, stop=None, timezone=UTC, count=None):
    """
    This an alternative way to generating sets of Delorean objects with
    HOURLY stops
    """
    return stops(start=start, stop=stop, freq=HOURLY, timezone=timezone, count=count)


def range_monthly(start=None, stop=None, timezone=UTC, count=None):
    """
    This an alternative way to generating sets of Delorean objects with
    MONTHLY stops
    """
    return stops(start=start, stop=stop, freq=MONTHLY, timezone=timezone, count=count)


def range_yearly(start=None, stop=None, timezone=UTC, count=None):
    """
    This an alternative way to generating sets of Delorean objects with
    YEARLY stops
    """
    return stops(start=start, stop=stop, freq=YEARLY, timezone=timezone, count=count)


def stops(freq, interval=1, count=None, wkst=None, bysetpos=None,
          bymonth=None, bymonthday=None, byyearday=None, byeaster=None,
          byweekno=None, byweekday=None, byhour=None, byminute=None,
          bysecond=None, timezone=UTC, start=None, stop=None):
    """
    This will create a list of delorean objects the apply to
    setting possed in.
    """
    # check to see if datetimees passed in are naive if so process them
    # with given timezone.
    if is_datetime_naive(start) and is_datetime_naive(stop):
        pass
    else:
        raise DeloreanInvalidDatetime('Provide a naive datetime object')

    # if no datetimes are passed in create a proper datetime object for
    # start default because default in dateutil is datetime.now() :(
    if start is None:
        start = datetime_timezone(timezone)

    for dt in rrule(freq, interval=interval, count=count, wkst=wkst, bysetpos=bysetpos,
          bymonth=bymonth, bymonthday=bymonthday, byyearday=byyearday, byeaster=byeaster,
          byweekno=byweekno, byweekday=byweekday, byhour=byhour, byminute=byminute,
          bysecond=bysecond, until=stop, dtstart=start):
        # make the delorean object
        # yield it.
        # doing this to make sure delorean receives a naive datetime.
        dt = dt.replace(tzinfo=None)
        d = Delorean(datetime=dt, timezone=timezone)
        yield d


def epoch(s):
    dt = datetime.utcfromtimestamp(s)
    return Delorean(datetime=dt, timezone=UTC)


def flux():
    print("If you put your mind to it, you can accomplish anything.")


def utcnow():
    """
    Return a delorean object, with utcnow as the datetime
    """
    return Delorean()


def now():
    """
    Return a delorean object, with utcnow as the datetime
    """
    return utcnow()
