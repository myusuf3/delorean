from datetime import datetime
from pytz import timezone
from dateutil.parser import parse
from dateutil.rrule import rrule
from .exceptions import DeloreanInvalidDatetime

from .data import Delorean, is_datetime_naive

UTC = "UTC"


def capture(s, dayfirst=True, timezone=UTC):
    """
    Parse a string with a datetime in it and return a delorean object
    Optionally accept a TZ if not specificed all times will be assumed
    to be UTC
    """
    try:
        dt = parse(s, dayfirst=dayfirst, ignoretz=True)
    except:
        # raise a parsing error.
        pass
    do = Delorean(datetime=dt, timezone=timezone)
    return do


def stops(freq, interval=1, count=None, wkst=None, bysetpos=None,
          bymonth=None, bymonthday=None, byyearday=None, byeaster=None,
          byweekno=None, byweekday=None, byhour=None, byminute=None,
          bysecond=None, timezone=UTC, start=None, until=None):
    """
    This will create a list of delorean objects the apply to
    setting possed in.
    """
    tz = timezone(timezone)
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
        start = datetime.utcnow()

    for dt in rrule(freq, interval=1, count=count, wkst=None, bysetpos=None,
          bymonth=None, bymonthday=None, byyearday=None, byeaster=None,
          byweekno=None, byweekday=None, byhour=None, byminute=None,
          bysecond=None, until=until, dtstart=start):
        # make the delorean object
        # yield it.

        d = Delorean(datetime=dt, timezone=timezone)
        yield d

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

