from dateutil.parser import parse
from dateutil.rrule import rrule
from .data import Delorean

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


def range(freq, start, stop, interval):
    """
    This will create a list of delorean objects the apply to
    setting possed in.
    """
    pass


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

