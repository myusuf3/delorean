from datetime import datetime

from pytz import timezone
from dateutil.parser import parse as capture
from dateutil.rrule import rrule
from .exceptions import DeloreanInvalidDatetime

from .data import Delorean, is_datetime_naive, datetime_timezone

UTC = "UTC"
utc = timezone("utc")


def parse(s, dayfirst=True):
    """
    Parse a string with a datetime in it and return a delorean object

    If a timezone is detected in the parse it will converted to UTC,
    and a Delorean object with that datetime and timezone will be
    returned.
    """
    try:
        dt = capture(s, dayfirst=dayfirst)
    except:
        # raise a parsing error.
        raise ValueError("Unknown string format")
    if dt.tzinfo is None:
        # assuming datetime object passed in is UTC
        do = Delorean(datetime=dt, timezone=UTC)
    else:
        dt = utc.normalize(dt)
        # makeing dt naive so we can pass it to Delorean
        dt = dt.replace(tzinfo=None)
        # if parse string has tzinfo we return a normalized UTC
        # delorean object that represents the time.
        do = Delorean(datetime=dt, timezone=UTC)
    return do


def stops(freq, interval=1, count=None, wkst=None, bysetpos=None,
          bymonth=None, bymonthday=None, byyearday=None, byeaster=None,
          byweekno=None, byweekday=None, byhour=None, byminute=None,
          bysecond=None, tz=UTC, start=None, until=None):
    """
    This will create a list of delorean objects the apply to
    setting possed in.
    """
    # check to see if datetimees passed in are naive if so process them
    # with given timezone.
    if is_datetime_naive(start) and is_datetime_naive(until):
        # start = tz.localize(start)
        # until = tz.localize(until)
        pass
    else:
        raise DeloreanInvalidDatetime('Provide a naive datetime object')

    # if no datetimes are passed in create a proper datetime object for
    # start default because default in dateutil is datetime.now() :(
    if start is None:
        start = datetime_timezone(tz)

    for dt in rrule(freq, interval=interval, count=count, wkst=None, bysetpos=None,
          bymonth=None, bymonthday=None, byyearday=None, byeaster=None,
          byweekno=None, byweekday=None, byhour=None, byminute=None,
          bysecond=None, until=until, dtstart=start):
        # make the delorean object
        # yield it.
        # doing this to make sure delorean receives a naive datetime.
        dt = dt.replace(tzinfo=None)
        d = Delorean(datetime=dt, timezone=tz)
        yield d


def epoch(s):
    dt = datetime.utcfromtimestamp(s)
    return Delorean(datetime=dt, timezone=UTC)


def flux():
    print "If you put your mind to it, you can accomplish anything."


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

