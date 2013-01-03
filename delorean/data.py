from datetime import datetime
from pytz import timezone


def utc_with_timezone(tz="UTC"):
    """
    This method returns utcnow with appropriate timezone
    """
    utc = timezone(tz)
    utc_datetime = datetime.utcnow()
    return utc.localize(utc_datetime)


def localize(dt, tz):
    """
    Given a datetime object this method will return a datetime object
    """
    utc = timezone(tz)
    utc_datetime = datetime.utcnow()
    return utc.localize(utc_datetime)


def normalize(self, tz):
    """
    Given a object with a timezone return a datetime object
    normalized to the proper timezone.

    This means take the give datetime and return the datetime shifted
    to match the specificed timezone.
    """
    tz = timezone(tz)
    self._datetime = tz.normalize(self.datetime)
    self._date.set_date(self._datetime.date())
    return self


class Delorean(object):
    """ The :class" `Delorean <Delorean>` object. It carries out all
    functionality of the Delorean.
    """
    def __init__(self, dt=None, tz=None):
        # maybe set timezone on the way in here. if here set it if not
        # use UTC
        self._tz = tz
        self._dt = dt
        if tz is None:
            self._tz = "UTC"
        if dt is None:
            self._dt = utc_with_timezone()

    def __repr__(self):
        return '<Delorean[%s]>' % (self._dt)

    def date(self):
        """
        This method returns the actual date object associated with class
        """
        return self._dt.date()

    def datetime(self):
        """
        This method returns the actual datetime object associated with class
        """
        return self._dt.get_datetime()
