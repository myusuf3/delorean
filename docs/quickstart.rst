Usage
=====
`Delorean` aims to provide you with convient ways to get significant dates and times and easy ways to move dates from state to state.

In order to get the most of the documentation we will define some terminology.

1. **naive datetime** -- a datetime object without a timezone.
2. **localized datetime** -- a datetime object with a timezone.
3. **localizing** -- associating a naive datetime object with a timezone.
4. **normalizing** -- shifting a  localized datetime object from one timezone to another, this changes both tzinfo and datetime object.


Making Some Time
^^^^^^^^^^^^^^^^

Making time with `delorean` is much easier than in life.

Start with importing delorean::

    >>> from delorean import Delorean

Now lets create a create `datetime` with the current datetime and UTC timezone
::

    >>> d = Delorean()
    >>> d
    Delorean(datetime=datetime.datetime(2013, 1, 12, 6, 10, 33, 110674),  timezone='UTC')

Do you want to normalize this timezone to another timezone? Simply do the following
::

   >>> d = d.shift("US/Eastern")
   >>> d
   Delorean(datetime=datetime.datetime(2013, 1, 12, 1, 10, 38, 102223), timezone='US/Eastern')

Now that you have successfully shifted the timezone you can easily return a localized datetime object or date with ease.
::

    >>> d.datetime
    datetime.datetime(2013, 1, 12, 01, 10, 38, 102223, tzinfo=<DstTzInfo 'US/Eastern' EST-1 day, 19:00:00 STD>)
    >>> d.date
    datetime.date(2013, 1, 12)

For the purists out there you can do things like so.
::

    >>> d.naive
    datetime.datetime(2013, 1, 12, 1, 10, 38, 102223)
    >>> d.epoch
    1357971038.102223

You can also create Delorean object using unix timestamps.

::

    from delorean import epoch
    >>> epoch(1357971038.102223).shift("US/Eastern")
    Delorean(datetime=datetime.datetime(2013, 1, 12, 1, 10, 38, 102223), timezone='US/Eastern')

As you can see `delorean` returns a Delorean object which you can shift to the appropriate timezone to get back your original datetime object from above.


.. note::

    If you are comparing Delorean objects the time since epoch will be used internally
    for comparison. This allows for the greatest accuracy when comparing Delorean
    objects from different timezones!

`Delorean` also now accepts localized datetimes. This means if you had a previously localized datetime object, Delorean will now accept these values and set the associated timezone and datetime information on the Delorean object.

.. note::

    If you pass in a timezone with a localized datetime the timezone will be ignored, since the datetime object you are passing already has timezone information already associated with it.


::

    >>> tz = timezone("US/Pacific")
    >>> dt = tz.localize(datetime.utcnow())
    datetime.datetime(2013, 3, 16, 5, 28, 11, 536818, tzinfo=<DstTzInfo 'US/Pacific' PDT-1 day, 17:00:00 DST>)
    >>> d = Delorean(datetime=dt)
    >>> d
    Delorean(datetime=datetime.datetime(2013, 3, 16, 5, 28, 11, 536818), timezone='US/Pacific')
    >>> d = Delorean(datetime=dt, timezone="US/Eastern")
    >>> d
    Delorean(datetime=datetime.datetime(2013, 3, 16, 5, 28, 11, 536818), timezone='US/Pacific')

Time Arithmetic
^^^^^^^^^^^^^^^

`Delorean` can also handle timedelta arithmetic. A timedelta may be added to or subtracted from a `Delorean` object.
Additionally, you may subtract a `Delorean` object from another Delorean object to obtain the timedelta between them.

::

    >>> d = Delorean()
    >>> d
    Delorean(datetime=datetime.datetime(2014, 6, 3, 19, 22, 59, 289779), timezone='UTC')
    >>> d += timedelta(hours=2)
    >>> d
    Delorean(datetime=datetime.datetime(2014, 6, 3, 21, 22, 59, 289779), timezone='UTC')
    >>> d - timedelta(hours=2)
    Delorean(datetime=datetime.datetime(2014, 6, 3, 19, 22, 59, 289779), timezone='UTC')
    >>> d2 = d + timedelta(hours=2)
    >>> d2 - d
    datetime.timedelta(0, 7200)

`Delorean` objects are considered equal if they represent the same time in UTC.

::

    >>> d1 = Delorean(datetime(2015, 1, 1), timezone='US/Pacific')
    >>> d2 = Delorean(datetime(2015, 1, 1, 8), timezone='UTC')
    >>> d1 == d2
    True

Natural Language
^^^^^^^^^^^^^^^^
`Delorean` provides many ways to get certain date relative to another, often getting something simple like the next year or the next thursday can be quite troublesome.

`Delorean` provides several conveniences for this type of behaviour. For example if you wanted to get next Tuesday from today you would simply do the following
::

    >>> d = Delorean()
    >>> d
    Delorean(datetime=datetime.datetime(2013, 1, 20, 19, 41, 6, 207481), timezone='UTC')
    >>> d.next_tuesday()
    Delorean(datetime=datetime.datetime(2013, 1, 22, 19, 41, 6, 207481), timezone='UTC')

Last Tuesday? Two Tuesdays ago at midnight? No problem.

::

    >>> d.last_tuesday()
    Delorean(datetime=datetime.datetime(2013, 1, 15, 19, 41, 6, 207481), timezone='UTC')
    >>> d.last_tuesday(2).midnight
    datetime.datetime(2013, 1, 8, 0, 0, tzinfo=<UTC>)


Replace Parts
^^^^^^^^^^^^^
Using the `replace` method on `Delorean` objects, we can replace the `hour`, `minute`, `second`, `year` etc
like the the `replace` method on `datetime`.

::

    >>> d = Delorean(datetime(2015, 1, 1, 12, 15), timezone='UTC')
    >>> d.replace(hour=8)
    Delorean(datetime=datetime.datetime(2015, 1, 1, 8, 15), timezone='UTC')


Truncation
^^^^^^^^^^
Often we dont care how many milliseconds or even seconds that are present in our datetime object. For example it is a nuisance to retrieve `datetimes` that occur in the same minute. You would have to go through the annoying process of replacing zero for the units you don't care for before doing a comparison.


`Delorean` comes with a method that allows you to easily truncate to different unit of time: millisecond, second, minute, hour, etc.
::

    >>> d = Delorean()
    >>> d
    Delorean(datetime=datetime.datetime(2013, 1, 21, 3, 34, 30, 418069), timezone='UTC')
    >>> d.truncate('second')
    Delorean(datetime=datetime.datetime(2013, 1, 21, 3, 34, 30), timezone='UTC')
    >>> d.truncate('hour')
    Delorean(datetime=datetime.datetime(2013, 1, 21, 3, 0), timezone='UTC')

Though it might seem obvious `delorean` also provides truncation to the month and year levels as well.
::

    >>> d = Delorean(datetime=datetime(2012, 5, 15, 03, 50, 00, 555555), timezone="US/Eastern")
    >>> d
    Delorean(datetime=datetime.datetime(2012, 5, 15, 3, 50, 0, 555555), timezone='US/Eastern')
    >>> d.truncate('month')
    Delorean(datetime=datetime.datetime(2012, 5, 1), timezone='US/Eastern')
    >>> d.truncate('year')
    Delorean(datetime=datetime.datetime(2012, 1, 1), timezone='US/Eastern')

Strings and Parsing
^^^^^^^^^^^^^^^^^^^
Another pain is dealing with strings of datetimes. `Delorean` can help you parse all the datetime strings you get from various APIs.
::

    >>> from delorean import parse
    >>> parse("2011/01/01 00:00:00 -0700")
    Delorean(datetime=datetime.datetime(2011, 1, 1, 7), timezone='UTC')

As shown above if the string passed has offset data `delorean` will convert the resulting object to UTC, if there is no timezone information passed in UTC is assumed.


Ambiguous cases
"""""""""""""""

There might be cases where the string passed to parse is a bit ambiguous for example. In the case where `2013-05-06` is passed is this May 6th, 2013 or is June 5th, 2013?

`Delorean` makes the assumptions that ``dayfirst=True`` and ``yearfirst=True`` this will lead to the following precedence.


    If dayfirst is True and yearfirst is True:

    - YY-MM-DD
    - DD-MM-YY
    - MM-DD-YY

So for example with default parameters `Delorean` will return '2013-05-06' as May 6th, 2013.
::

    >>> parse("2013-05-06")
    Delorean(datetime=datetime.datetime(2013, 5, 6), timezone='UTC')

Here are the precedence for the remaining combinations of ``dayfirst`` and ``yearfirst``.

    If dayfirst is False and yearfirst is False:

    - MM-DD-YY
    - DD-MM-YY
    - YY-MM-DD

    If dayfirst is True and yearfirst is False:

    - DD-MM-YY
    - MM-DD-YY
    - YY-MM-DD

    If dayfirst is False and yearfirst is True:

    - YY-MM-DD
    - MM-DD-YY
    - DD-MM-YY


Making A Few Stops
^^^^^^^^^^^^^^^^^^
Delorean wouldn't be complete without making a few stop in all the right places.
::

    >>> import delorean
    >>> from delorean import stops
    >>> for stop in stops(freq=delorean.HOURLY, count=10):    print stop
    ...
    Delorean(datetime=datetime.datetime(2013, 1, 21, 6, 25, 33), timezone='UTC')
    Delorean(datetime=datetime.datetime(2013, 1, 21, 7, 25, 33), timezone='UTC')
    Delorean(datetime=datetime.datetime(2013, 1, 21, 8, 25, 33), timezone='UTC')
    Delorean(datetime=datetime.datetime(2013, 1, 21, 9, 25, 33), timezone='UTC')
    Delorean(datetime=datetime.datetime(2013, 1, 21, 10, 25, 33), timezone='UTC')
    Delorean(datetime=datetime.datetime(2013, 1, 21, 11, 25, 33), timezone='UTC')
    Delorean(datetime=datetime.datetime(2013, 1, 21, 12, 25, 33), timezone='UTC')
    Delorean(datetime=datetime.datetime(2013, 1, 21, 13, 25, 33), timezone='UTC')
    Delorean(datetime=datetime.datetime(2013, 1, 21, 14, 25, 33), timezone='UTC')
    Delorean(datetime=datetime.datetime(2013, 1, 21, 15, 25, 33), timezone='UTC')

This allows you to do clever composition like daily, hourly, etc. This method is a generator that produces `Delorean` objects. Excellent for things like getting every Tuesday for the next 10 weeks, or every other hour for the next three months.

With Power Comes
""""""""""""""""

Now that you can do this you can also specify ``timezones`` as well ``start`` and ``stop`` dates for iteration.
::

    >>> import delorean
    >>> from delorean import stops
    >>> from datetime import datetime
    >>> d1 = datetime(2012, 5, 06)
    >>> d2 = datetime(2013, 5, 06)

.. note::

   The ``stops`` method only accepts naive datetime ``start`` and ``stop`` values.

Now in the case where you provide `timezone`, `start`, and `stop` all is good in the world!
::

    >>> for stop in stops(freq=delorean.DAILY, count=10, timezone="US/Eastern", start=d1, stop=d2):    print stop
    ...
    Delorean(datetime=datetime.datetime(2012, 5, 6), timezone='US/Eastern')
    Delorean(datetime=datetime.datetime(2012, 5, 7), timezone='US/Eastern')
    Delorean(datetime=datetime.datetime(2012, 5, 8), timezone='US/Eastern')
    Delorean(datetime=datetime.datetime(2012, 5, 9), timezone='US/Eastern')
    Delorean(datetime=datetime.datetime(2012, 5, 10), timezone='US/Eastern')
    Delorean(datetime=datetime.datetime(2012, 5, 11), timezone='US/Eastern')
    Delorean(datetime=datetime.datetime(2012, 5, 12), timezone='US/Eastern')
    Delorean(datetime=datetime.datetime(2012, 5, 13), timezone='US/Eastern')
    Delorean(datetime=datetime.datetime(2012, 5, 14), timezone='US/Eastern')
    Delorean(datetime=datetime.datetime(2012, 5, 15), timezone='US/Eastern')


.. note::

   if no ``start`` or ``timezone`` value is specified start is assumed to be localized UTC object. If timezone is provided
   a normalized UTC to the correct timezone.

Now in the case where a naive stop value is provided you can see why the follow error occurs if you take into account the above note.

.. doctest::
    :options: +SKIP

    >>> for stop in stops(freq=delorean.DAILY, timezone="US/Eastern", stop=d2):    print stop
    ...
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "delorean/interface.py", line 63, in stops
        bysecond=None, until=until, dtstart=start):
    TypeError: can't compare offset-naive and offset-aware datetimes

You will be better off in scenarios of this nature to skip using either and use count to limit the range of the values returned.

.. doctest::
    :options: +SKIP

    >>> from delorean import stops
    >>> for stop in stops(freq=delorean.DAILY, count=2, timezone="US/Eastern"):    print stop
    ...
    Delorean(datetime=datetime.datetime(2013, 1, 22, 0, 10, 10), timezone='US/Eastern')
    Delorean(datetime=datetime.datetime(2013, 1, 23, 0, 10, 10), timezone='US/Eastern')
