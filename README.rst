Delorean: Time Travel Made Easy
============================

``delorean`` is a library for clearing up the confusion that is the ``datetime`` module. It will provide natural language improvements for manipulating time. 

.. image:: https://github.com/

Usage
=====

Note: This API is in flux still trying to soldify API.
------------------------------------------------------

The overall goal is to improve date and time manipulations, as well as help create a simple way for detecting timezones in various areas as well as providing standardized utc

::

	import delorean

	'''
	All date, times, and datetimes returned are all UTC, if you require, something localized
	you are to set it yourself. This will provided via API, this is done to simplify and standardize
	the time library you are always aware of what you are working with.
	'''

	>>> today = delorean.today()
	<DelorianDateTime: 2011-09-19>

	>>> tomorrow = today.tomorrow()
	<DelorianDateTime: 2011-09-20>

	>>> tomorrow.date()
	2011-09-20 (python Date Object)

	>>>tomorrow.datetime()
	2011-09-20 00:00:00  (python DateTime Object) significant bits are zeroed out cause we only started with a date, but its still a datetime object.

	>>>tomorow.time()
	00:00:00 (python Time Object) since only a date object was created with date)
	>>> next_year = delorean.nextyear()
	<DelorianDateTime: 2012-09-19>


	>>> gmt = delorean.time()
	08:06:53 (python Time Object) 
	>>> us_eastern = delorean.time(east_coast) this accepts 
	13:06:53(python Time Object) 
	>>> now = delorian.datetime().now()
	2011-09-19 08:06:53 (python DateTime Object)
	>>> utc = delorian.datetime().utcnow()
	2011-09-19 08:06:53 (python DateTime Object)
	>>> local = delorian.localnow()
	2011-09-19 13:06:53 (python DateTime Object) localized. tz set using local. all accept tz value like 'America/Montreal'



