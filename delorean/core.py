from datetime import timedelta, datetime, time, date, tzinfo





class Delorean(object):
	""" The :class" `Delorean <Delorean>` object. It carries out all 
	functionality of the Delorean.
	"""
	def __init__(self):
		#: time object
		self.time = time

		#:datetime object
		self.datetime = datetime.utcnow()
	
	def __repr__(self):
		return '<Delorean[%s]' % (self.date)
	
	def today():
		return datetime.utcnow()
	
	def tomorrow():
		one_day = timedelta(days=1)
		today = datetime.datetime.utcnow()
		tomorow = today + one_day
		return tommorrow
	
	def future(current_datetime, days=0, months=0, years=0, 
		hours=0, minutes=0, seconds=0, milliseconds=0, weeks=0):

		travel = timedelta()
