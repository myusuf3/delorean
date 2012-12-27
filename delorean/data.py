from datetime import datetime
from pytz import timezone


def utc_with_timezone():
    """
    This method returns utcnow with appropriate timezone
    """
    utc = timezone("UTC")
    utc_datetime = datetime.utcnow()
    return utc.localize(utc_datetime)


class Delorean(object):
    """ The :class" `Delorean <Delorean>` object. It carries out all
    functionality of the Delorean.
    """
    def __init__(self,
        dt=None,
        tz=None,
        ):
        # maybe set timezone on the way in here. if here set it if not
        # use UTC
        self._tz = tz
        self._dt = dt
        if tz is None:
            self._tz = "UTC"
        if dt is None:
            self._dt = utc_with_timezone()


    def __repr__(self):
        return '<Delorean[%s]>' % (self._tz)

    def date(self):
        """
        This method returns the actual date object associated with class
        """
        return self._datetime.date()

    def datetime(self):
        """
        This method returns the actual date object associated with class
        """
        return self._datetime.get_datetime()

    def localize(self, timezone):
        """
        Given a datetime object this method will return a datetime object
        """

        return self

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


class DeloreanDate(object):
    """
    This class encapulates the data associated with dates.
    """
    def __init__(self, dt=None):
        if dt is None:
            self._date = date.today()
        if isinstance(dt, date):
            self._date = dt
        else:
            # raise some error
            pass

    @property
    def date(self):
        """
        Returns the date associated with the DeloreanDate object
        """
        return self._date

    @date.setter
    def set_date(self, date):
        self._date = date


    # functions to move dates up and down
    # dateutils



class DeloreanDatetime(object):
    """
    This class encapulates the data associated with datetimes.
    """
    def __init__(self, dt=None, tm=None):
        if dt is None and tm is None:
            self._datetime = self._localize_utc()
        if dt is None and tm is not None:
            self._datetime = datetime.utcnow()
            self._localize(tm)
        if dt is not None and tm is None:
            # decide if I want to raise an error.
            print "Error"

    def _localize_utc(self):
        """
        localizes the DeloreanDatetime object UTC
        """
        UTC = timezone("UTC")
        return UTC.localize(datetime.utcnow())

    def _localize(self, tz):
        """
        Given the a timezone this method localizes DeloreanDatetime to
        the given timezone, given in the form of string or object

        This method just super imposses tzinfo on given datetime object
        it is up to user to make sure the time is correct.
        """
        timezone_object = timezone(tz)
        self._datetime = timezone_object.localize(self._datetime)

    def get_datetime(self):
        return self._datetime



