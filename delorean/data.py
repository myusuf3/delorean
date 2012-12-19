from datetime import datetime, date,
from pytz import timezone, common_timezones


class Delorean(object):
    """ The :class" `Delorean <Delorean>` object. It carries out all
    functionality of the Delorean.
    """
    def __init__(self,
        timezone=None,
        date=None,
        datetime=None,
        time=None,
        ):
        self._date = date
        self._datetime = datetime
        self._time = time
        pass

        # if timezone is passed in check to see if it is contained
        # in the pytz timezones except if not.

    def __repr__(self):
        return '<Delorean[%s]>'

    def date(self):
        """
        This method returns the actual date object associated with class
        """
        return self._date

    def datetime(self):
        """
        This method returns the actual date object associated with class
        """
        return self._datetime

    def localize(self, timezone):
        """
        Given a datetime object this method will return a datetime object
        """
        return self

    def normalize(self, timezone):
        """
        Given a object with a timezone return a datetime object
        normalized to the proper timezone.

        This means take the give datetime and return the datetime shifted
        to match the specificed timezone.
        """
        return self


class DeloreanDate(object):
    """
    This class encapulates the data associated with dates.
    """
    def __init__(self, deldate=None):
        if deldate is None:
            self._date = date.today()
        if isinstance(deldate, date):
            self._date = deldate
        else:
            # raise some error
            pass


    # functions to move dates up and down
    # dateutils


class DeloreanDatetime(object):
    """
    This class encapulates the data associated with datetimes.
    """
    def __init(self, dt=None, timezone=None):
        if dt is None and timezone is None:
            self._datetime = self._localize_utc()
        if dt is None and timezone is not None:
            self._datetime = datetime.utcnow()
            self._localize(timezone)

    def _localize_utc(self):
        """
        localizes the DeloreanDatetime object UTC
        """
        UTC = timezone("UTC")
        return UTC.localize(datetime.utcnow())

    def localize(self, tz):
        """
        Given the a timezone this method localizes DeloreanDatetime to
        the given timezone, given in the form of string or object

        This method just super imposses tzinfo on given datetime object
        it is up to user to make sure the time is correct.
        """
        timezone_object = timezone(tz)
        self._datetime = timezone_object.localize(self._datetime)
        return self

