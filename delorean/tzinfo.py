from datetime import datetime, timedelta, tzinfo

_ZERO = timedelta(0)


class DeloreanTzInfo(tzinfo):
	_utcoffset = None
	_tzname = None
	zone = None

	def __str__(self):
		return self.zone


class DeloreanStaticTzInfo(DeloreanTzInfo):
	""" This is for static timezomes"""

	def fromutc(self, dt):
		return (dt + self._utcoffset).replace(tzinfo=self)
	
	def utcoffset(self, dt, is_dst=None):
		return self._utcoffset
	
	def dst(self, dt, is_dst=None):
		return _ZERO

	def tzname(self, dt, is_dst=None):
		return self._tzname
	
	def localize(self, dt, is_dst=False):
		"""This method will localize the given datetime value to """
		if dt.tzinfo is not None:
			raise ValueError("tzinfo has already been set!")
		return dt.replace(tzinfo=self)
	
	def normalize(self, df, is_dst=False):
		if dt.tzinfo is self:
			return dt
		if dt.tzinfo is None:
			raise ValueError("tzinfo has not been set!")
		return dt.astimezone(self)
	
	def __repr__(self):
		return '<DeloreanStaticTzInfo %r>' % (self.zone,)

class DeloreanVariableTzInfo(DeloreanTzInfo):
	pass

