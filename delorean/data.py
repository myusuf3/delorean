from datetime import datetime
from pytz import timezone


def parse(s, tz=None):
    """
    Parse a string with a datetime in it and return a delorean object
    Optionally accept a TZ
    """
    pass


def utcnow():
    """
    Return a delorean object, with utcnow as the datetime
    """
    pass


def now():
    """
    Return a delorean object, with utcnow as the datetime
    """
    return utcnow()


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
    _VALID_SHIFTS = ('day', 'week', 'month', 'year', 'monday', 'tuesday',
                     'wednesday', 'thursday', 'friday', 'saturday', 'sunday')

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

    def __getattr__(self, name):
        """
        Implement __getattr__ to call `last` or `first` when function does not
        exist
        """
        func_parts = name.split('_')

        if len(func_parts) != 2:
            raise AttributeError

        try:
            func = getattr(self, func_parts[0], None)
            if not func or func_parts[1] not in self._VALID_SHIFTS:
                raise AttributeError

            return func
        except:
            raise AttributeError

    def last(self, shift_by, shift_by_multiple=None):
        """
        Shift datetime back by some unit in _VALID_SHIFTS and shift that amount
        by some multiple, defined by shift_by_multiple
        """
        pass

    def next(self, shift_by, shift_by_multiple=None):
        """
        Shift datetime back by some unit in _VALID_SHIFTS and shift that amount
        by some multiple, defined by shift_by_multiple
        """
        pass

    def truncate(self, s):
        """
        Truncate the delorian object by s (hour, day, week, month, etc)
        """
        pass

    @property
    def date(self):
        """
        This method returns the actual date object associated with class
        """
        return self._dt.date()

    @property
    def datetime(self):
        """
        This method returns the actual datetime object associated with class
        """
        return self._dt.get_datetime()
