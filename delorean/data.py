import sys
from datetime import datetime
from dateutil.relativedelta import relativedelta
from .exceptions import DeloreanInvalidTimezone, DeloreanInvalidDatetime
from functools import partial, update_wrapper

import pytz
from pytz import timezone

UTC = "UTC"
utc = timezone("UTC")


def is_datetime_naive(dt):
    """
    This method returns true if the datetime is naive else returns false
    """
    if dt is None:
        return True

    if dt.tzinfo is None:
        return True
    else:
        return False


def _move_datetime(dt, direction, delta):
    """
    Move datetime given delta by given direction
    """
    if direction == 'next':
        dt = dt + delta
    elif direction == 'last':
        dt = dt - delta
    else:
        pass
        # raise some delorean error here
    return dt


def move_datetime_day(dt, direction, num_shifts):
    delta = relativedelta(days=+num_shifts)
    return _move_datetime(dt, direction, delta)


def move_datetime_namedday(dt, direction, unit):
    """
    """
    TOTAL_DAYS = 7
    days = {
        'monday': 1,
        'tuesday': 2,
        'wednesday': 3,
        'thursday': 4,
        'friday': 5,
        'saturday': 6,
        'sunday': 7,
    }

    current_day = days[dt.strftime('%A').lower()]
    target_day = days[unit.lower()]

    if direction == 'next':
        if current_day < target_day:
            delta_days = target_day - current_day
        else:
            delta_days = (target_day - current_day) + TOTAL_DAYS
    elif direction == 'last':

        if current_day <= target_day:
            delta_days = (current_day - target_day) + TOTAL_DAYS
        else:
            delta_days = current_day - target_day

    delta = relativedelta(days=+delta_days)
    return _move_datetime(dt, direction, delta)


def move_datetime_month(dt, direction, num_shifts):
    """
    Move datetime 1 month in the chosen direction.
    unit is a no-op, to keep the API the same as the day case
    """
    delta = relativedelta(months=+num_shifts)
    return _move_datetime(dt, direction, delta)


def move_datetime_week(dt, direction, num_shifts):
    """
    Move datetime 1 week in the chosen direction.
    unit is a no-op, to keep the API the same as the day case
    """
    delta = relativedelta(weeks=+num_shifts)
    return _move_datetime(dt, direction, delta)


def move_datetime_year(dt, direction, num_shifts):
    """
    Move datetime 1 year in the chosen direction.
    unit is a no-op, to keep the API the same as the day case
    """
    delta = relativedelta(years=+num_shifts)
    return _move_datetime(dt, direction, delta)


def datetime_timezone(tz):
    """
    This method returns utcnow with appropriate timezone, or normalized
    to the correct timezone if provided.
    """
    utc_datetime_naive = datetime.utcnow()
    # return a localized datetime to UTC
    utc_localized_datetime = localize(utc_datetime_naive, UTC)
    # normalize the datetime to given timezone
    normalized_datetime = normalize(utc_localized_datetime, tz)
    return normalized_datetime


def localize(dt, tz):
    """
    Given a naive datetime object this method will return a localized
    datetime object
    """
    tz = timezone(tz)
    return tz.localize(dt)


def normalize(dt, tz):
    """
    Given a object with a timezone return a datetime object
    normalized to the proper timezone.

    This means take the give datetime and return the datetime shifted
    to match the specificed timezone.
    """
    tz = timezone(tz)
    dt = tz.normalize(dt)
    return dt


class Delorean(object):
    """ The :class" `Delorean <Delorean>` object. It carries out all
    functionality of the Delorean.
    """
    _VALID_SHIFT_DIRECTIONS = ('last', 'next')
    _VALID_SHIFT_UNITS = ('day', 'week', 'month', 'year', 'monday', 'tuesday',
                          'wednesday', 'thursday', 'friday', 'saturday',
                          'sunday')

    def __init__(self, datetime=None, timezone=None):
        # maybe set timezone on the way in here. if here set it if not
        # use UTC
        self._tz = timezone
        self._dt = datetime

        if is_datetime_naive(datetime):
            pass
        else:
            pass
            # raise a value error since you are passing a localized
            # datetime
            raise DeloreanInvalidDatetime('Provide a naive datetime object')

        if timezone is None and datetime is None:
            self._tz = UTC
            self._dt = datetime_timezone(UTC)
        elif timezone is not None and datetime is None:
            # create utctime then normalize to tz
            self._tz = timezone
            self._dt = datetime_timezone(timezone)
        elif timezone is None and datetime is not None:
            raise DeloreanInvalidTimezone('Provide a valid timezone')
        else:
            # passed in naive datetime and timezone
            # that correspond accordingly
            self._tz = timezone
            self._dt = localize(datetime, timezone)

    def __repr__(self):
        return 'Delorean(datetime=%s, timezone=%s)' % (self._dt, self._tz)

    def __eq__(self, other):
        # test this.
        return self._dt == other._dt and self._tz == other._tz

    def __getattr__(self, name):
        """
        Implement __getattr__ to call `shift_date` function when function
        called does not exist
        """
        func_parts = name.split('_')
        # is the func we are trying to call the right length?
        if len(func_parts) != 2:
            raise AttributeError

        # is the function we are trying to call valid?
        if (func_parts[0] not in self._VALID_SHIFT_DIRECTIONS or
                func_parts[1] not in self._VALID_SHIFT_UNITS):
            return AttributeError

        # dispatch our function
        func = partial(self._shift_date, func_parts[0], func_parts[1])
        # update our partial with self.shift_date attributes
        update_wrapper(func, self._shift_date)
        return func

    def _shift_date(self, direction, unit, *args):
        """
        Shift datetime in `direction` in _VALID_SHIFT_DIRECTIONS and by some
        unit in _VALID_SHIFTS and shift that amount by some multiple,
        defined by by args[0] if it exists
        """
        this_module = sys.modules[__name__]

        num_shifts = 1
        if len(args) > 0:
            num_shifts = int(args[0])

        if unit in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                    'saturday', 'sunday']:
            shift_func = move_datetime_namedday
            dt = shift_func(self._dt, direction, unit)
            if num_shifts > 1:
                for n in range(num_shifts - 1):
                    dt = shift_func(dt, direction, unit)
        else:
            shift_func = getattr(this_module, 'move_datetime_%s' % unit)
            dt = shift_func(self._dt, direction, num_shifts)

        return Delorean(datetime=dt.replace(tzinfo=None), timezone=self._tz)

    def timezone(self):
        """
        This method return a valid pytz timezone object or raises Invalid timezone
        error.
        """
        if self._tz is None:
            return None
        try:
            return timezone(self._tz)
        except pytz.exceptions.UnknownTimeZoneError:
            # raise some delorean error
            raise DeloreanInvalidTimezone('Provide a valid timezone')

    def truncate(self, s):
        """
        Truncate the delorian object to the nearest s
        (second, minute, hour, day, month, year)
        """
        if s is 'second':
            self._dt = self._dt.replace(microsecond=0)
        elif s is 'minute':
            self._dt = self._dt.replace(second=0, microsecond=0)
        elif s is 'hour':
            self._dt = self._dt.replace(minute=0, second=0, microsecond=0)
        elif s is 'day':
            self._dt = self._dt.replace(hour=0, minute=0, second=0, microsecond=0)
        elif s is 'month':
            self._dt = self._dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        elif s is 'year':
            self._dt = self._dt.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            raise ValueError("Invalid truncation level")

        return self

    def next_day(self, days):
        dt = self._dt + relativedelta(days=+days)
        dt = dt.replace(tzinfo=None)
        return Delorean(datetime=dt, timezone=self._tz)

    def naive(self):
        """
        Returns a naive datetime object from the Delorean object, this
        method simply converts localize datetime to UTC and removes
        the tzinfo that is associated with it.
        """
        return utc.normalize(self._dt).replace(tzinfo=None)

    def midnight(self):
        """
        This method returns midnight of the particular Delorean object
        """
        return self._dt.replace(hour=0, minute=0, second=0, microsecond=0)

    def shift(self, tz):
        """
        This method shifts the timezone from the current timezone to the
        specified timezone
        """
        try:
            zone = timezone(tz)
        except pytz.UnknownTimeZoneError:
            raise DeloreanInvalidTimezone('Provide a valid timezone')
        self._tz = tz
        self._dt = zone.normalize(self._dt)
        return self

    def epoch(self):
        """
        This method returns the total seconds since epoch.

        Usage::

            d = Delorean()
            d.epoch()
        """
        utc = timezone(UTC)
        epoch = utc.localize(datetime.utcfromtimestamp(0))
        dt = utc.normalize(self._dt)
        delta = dt - epoch
        return delta.total_seconds()

    @property
    def date(self):
        """
        This method returns the actual date object associated with
        the Delorean object
        """
        return self._dt.date()

    @property
    def datetime(self):
        """
        This method returns the actual datetime object associated with
        the Delorean object
        """
        return self._dt
