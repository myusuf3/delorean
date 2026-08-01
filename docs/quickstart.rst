Usage
=====
`Delorean` aims to provide you with convenient ways to get significant dates and times and easy ways to move dates from state to state.

In order to get the most of the documentation we will define some terminology.

1. **naive datetime** -- a datetime object without a timezone.
2. **localized datetime** -- a datetime object with a timezone.
3. **localizing** -- associating a naive datetime object with a timezone.
4. **normalizing** -- shifting a  localized datetime object from one timezone to another, this changes both tzinfo and datetime object.


Making Some Time
^^^^^^^^^^^^^^^^

Making time with `delorean` is much easier than in life.

Start with importing delorean:

.. doctest::

    >>> from delorean import Delorean

Now lets create a create `datetime` with the current datetime and UTC timezone

.. doctest::

    >>> d = Delorean()
    >>> d  # doctest: +ELLIPSIS
    Delorean(datetime=datetime.datetime(...), timezone='UTC')

Do you want to normalize this timezone to another timezone? Simply do the
following. The rest of this section works from one fixed moment rather than the
current time, so the values you see below are the ones you would get yourself.

.. doctest::

    >>> from datetime import datetime
    >>> d = Delorean(datetime(2013, 1, 12, 6, 10, 38, 102223), timezone='UTC')
    >>> d = d.shift("US/Eastern")
    >>> d
    Delorean(datetime=datetime.datetime(2013, 1, 12, 1, 10, 38, 102223), timezone='US/Eastern')

Now that you have successfully shifted the timezone you can easily return a localized datetime object or date with ease.

.. doctest::

    >>> d.datetime
    datetime.datetime(2013, 1, 12, 1, 10, 38, 102223, tzinfo=<DstTzInfo 'US/Eastern' EST-1 day, 19:00:00 STD>)
    >>> d.date
    datetime.date(2013, 1, 12)

For the purists out there you can do things like so. Note that ``naive``
converts to UTC before dropping the timezone, so it does not give you back the
local time shown above.

.. doctest::

    >>> d.naive
    datetime.datetime(2013, 1, 12, 6, 10, 38, 102223)
    >>> d.timestamp
    1357971038.102223

You can also create Delorean object using unix timestamps.

.. doctest::

    >>> from delorean import from_timestamp
    >>> from_timestamp(1357971038.102223).shift("US/Eastern")
    Delorean(datetime=datetime.datetime(2013, 1, 12, 1, 10, 38, 102223), timezone='US/Eastern')

.. note::

    ``timestamp`` and ``from_timestamp`` were previously named ``epoch``. Both
    old names still work and behave identically, but the new ones say what the
    value actually is (seconds since the Unix epoch, not the epoch itself) and
    avoid ``epoch`` meaning two opposite things.

As you can see `delorean` returns a Delorean object which you can shift to the appropriate timezone to get back your original datetime object from above.


.. note::

    If you are comparing Delorean objects the time since epoch will be used internally
    for comparison. This allows for the greatest accuracy when comparing Delorean
    objects from different timezones!

`Delorean` also now accepts localized datetimes. This means if you had a previously localized datetime object, Delorean will now accept these values and set the associated timezone and datetime information on the Delorean object.

.. note::

    If you pass in a timezone with a localized datetime the timezone will be ignored, since the datetime object you are passing already has timezone information already associated with it.


.. doctest::

    >>> from datetime import datetime
    >>> from pytz import timezone
    >>> tz = timezone("US/Pacific")
    >>> dt = tz.localize(datetime(2013, 3, 16, 5, 28, 11, 536818))
    >>> dt
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

.. doctest::

    >>> from datetime import timedelta
    >>> d = Delorean(datetime(2014, 6, 3, 19, 22, 59, 289779), timezone='UTC')
    >>> d
    Delorean(datetime=datetime.datetime(2014, 6, 3, 19, 22, 59, 289779), timezone='UTC')
    >>> d += timedelta(hours=2)
    >>> d
    Delorean(datetime=datetime.datetime(2014, 6, 3, 21, 22, 59, 289779), timezone='UTC')
    >>> d - timedelta(hours=2)
    Delorean(datetime=datetime.datetime(2014, 6, 3, 19, 22, 59, 289779), timezone='UTC')
    >>> d2 = d + timedelta(hours=2)
    >>> d2 - d
    datetime.timedelta(seconds=7200)

`Delorean` objects are considered equal if they represent the same time in UTC.

.. doctest::

    >>> d1 = Delorean(datetime(2015, 1, 1), timezone='US/Pacific')
    >>> d2 = Delorean(datetime(2015, 1, 1, 8), timezone='UTC')
    >>> d1 == d2
    True

Natural Language
^^^^^^^^^^^^^^^^
`Delorean` provides many ways to get certain date relative to another, often getting something simple like the next year or the next thursday can be quite troublesome.

`Delorean` provides several conveniences for this type of behaviour. For example if you wanted to get next Tuesday from today you would simply do the following

.. doctest::

    >>> d = Delorean(datetime(2013, 1, 20, 19, 41, 6, 207481), timezone='UTC')
    >>> d
    Delorean(datetime=datetime.datetime(2013, 1, 20, 19, 41, 6, 207481), timezone='UTC')
    >>> d.next_tuesday()
    Delorean(datetime=datetime.datetime(2013, 1, 22, 19, 41, 6, 207481), timezone='UTC')

Last Tuesday? Two Tuesdays ago at midnight? No problem.

.. doctest::

    >>> d.last_tuesday()
    Delorean(datetime=datetime.datetime(2013, 1, 15, 19, 41, 6, 207481), timezone='UTC')
    >>> d.last_tuesday(2).midnight
    Delorean(datetime=datetime.datetime(2013, 1, 8, 0, 0), timezone='UTC')


Daylight Saving Transitions
"""""""""""""""""""""""""""

Shifting moves the wall clock and then re-localizes the result, so crossing a
daylight saving boundary keeps the local time you asked for and updates the
offset to match. Below, 07:00 stays 07:00 and the timezone changes from EST to
EDT, which means the shift advanced 23 actual hours rather than 24.

.. doctest::

    >>> from pytz import timezone
    >>> eastern = timezone("US/Eastern")
    >>> d = Delorean(eastern.localize(datetime(2013, 3, 9, 7, 0)))
    >>> d.next_day().datetime
    datetime.datetime(2013, 3, 10, 7, 0, tzinfo=<DstTzInfo 'US/Eastern' EDT-1 day, 20:00:00 DST>)

Two kinds of local time need a tie-breaking rule, and `delorean` resolves both
of them to **standard** time.

A local time inside the spring-forward gap never happens. On 10 March 2013 the
Eastern clocks jumped straight from 02:00 EST to 03:00 EDT, so 02:30 has no
local reading at all. Shifting into it returns 02:30 EST, which is the instant
07:30 UTC.

.. doctest::

    >>> d = Delorean(eastern.localize(datetime(2013, 3, 9, 2, 30)))
    >>> d.next_day().datetime
    datetime.datetime(2013, 3, 10, 2, 30, tzinfo=<DstTzInfo 'US/Eastern' EST-1 day, 19:00:00 STD>)

A local time inside the autumn fall-back happens twice. On 3 November 2013,
01:30 occurs once as EDT and then again an hour later as EST. Shifting into it
returns the second, post-transition occurrence.

.. doctest::

    >>> d = Delorean(eastern.localize(datetime(2013, 11, 2, 1, 30)))
    >>> d.next_day().datetime
    datetime.datetime(2013, 11, 3, 1, 30, tzinfo=<DstTzInfo 'US/Eastern' EST-1 day, 19:00:00 STD>)

.. note::

    This rule is not specific to shifting. It applies wherever `delorean`
    localizes a naive datetime, because it comes from `pytz`'s ``is_dst=False``
    default. Pass an already-localized datetime if you need to choose the other
    side of a transition yourself.


Period Boundaries
^^^^^^^^^^^^^^^^^

`Delorean` objects can give you the first or last moment of the day, month or
year they fall in. Each returns a new `Delorean` object and leaves the original
untouched, so they compose with the shift methods above.

.. doctest::

    >>> d = Delorean(datetime(2015, 5, 15, 14, 30), timezone='UTC')
    >>> d.start_of_day
    Delorean(datetime=datetime.datetime(2015, 5, 15, 0, 0), timezone='UTC')
    >>> d.end_of_month
    Delorean(datetime=datetime.datetime(2015, 5, 31, 23, 59, 59, 999999), timezone='UTC')
    >>> d.start_of_year
    Delorean(datetime=datetime.datetime(2015, 1, 1, 0, 0), timezone='UTC')

``end_of_month`` knows how long each month is, including February in a leap
year.

.. doctest::

    >>> Delorean(datetime(2015, 2, 15), timezone='UTC').end_of_month
    Delorean(datetime=datetime.datetime(2015, 2, 28, 23, 59, 59, 999999), timezone='UTC')
    >>> Delorean(datetime(2024, 2, 15), timezone='UTC').end_of_month
    Delorean(datetime=datetime.datetime(2024, 2, 29, 23, 59, 59, 999999), timezone='UTC')

Because they return `Delorean` objects, they chain. The last day of the previous
month is:

.. doctest::

    >>> Delorean(datetime(2013, 5, 15), timezone='US/Eastern').last_month().end_of_month
    Delorean(datetime=datetime.datetime(2013, 4, 30, 23, 59, 59, 999999), timezone='US/Eastern')

The full set is ``start_of_day``, ``end_of_day``, ``start_of_month``,
``end_of_month``, ``start_of_year`` and ``end_of_year``, plus ``midnight``,
which is an alias of ``start_of_day``.


Replace Parts
^^^^^^^^^^^^^
Using the `replace` method on `Delorean` objects, we can replace the `hour`, `minute`, `second`, `year` etc
like the the `replace` method on `datetime`.

.. doctest::

    >>> d = Delorean(datetime(2015, 1, 1, 12, 15), timezone='UTC')
    >>> d.replace(hour=8)
    Delorean(datetime=datetime.datetime(2015, 1, 1, 8, 15), timezone='UTC')


Truncation
^^^^^^^^^^
Often we dont care how many milliseconds or even seconds that are present in our datetime object. For example it is a nuisance to retrieve `datetimes` that occur in the same minute. You would have to go through the annoying process of replacing zero for the units you don't care for before doing a comparison.


`Delorean` comes with a method that allows you to easily truncate to different unit of time: millisecond, second, minute, hour, etc.

.. doctest::

    >>> d = Delorean(datetime(2013, 1, 21, 3, 34, 30, 418069), timezone='UTC')
    >>> d
    Delorean(datetime=datetime.datetime(2013, 1, 21, 3, 34, 30, 418069), timezone='UTC')
    >>> d.truncate('second')
    Delorean(datetime=datetime.datetime(2013, 1, 21, 3, 34, 30), timezone='UTC')
    >>> d.truncate('hour')
    Delorean(datetime=datetime.datetime(2013, 1, 21, 3, 0), timezone='UTC')

Though it might seem obvious `delorean` also provides truncation to the month and year levels as well.

.. doctest::

    >>> d = Delorean(datetime=datetime(2012, 5, 15, 3, 50, 0, 555555), timezone="US/Eastern")
    >>> d
    Delorean(datetime=datetime.datetime(2012, 5, 15, 3, 50, 0, 555555), timezone='US/Eastern')
    >>> d.truncate('month')
    Delorean(datetime=datetime.datetime(2012, 5, 1, 0, 0), timezone='US/Eastern')
    >>> d.truncate('year')
    Delorean(datetime=datetime.datetime(2012, 1, 1, 0, 0), timezone='US/Eastern')

Strings and Parsing
^^^^^^^^^^^^^^^^^^^
Another pain is dealing with strings of datetimes. `Delorean` can help you parse all the datetime strings you get from various APIs.

.. doctest::

    >>> from delorean import parse
    >>> parse("2011/01/01 00:00:00 -0700")
    Delorean(datetime=datetime.datetime(2011, 1, 1, 0, 0), timezone=pytz.FixedOffset(-420))

As shown above if the string passed has offset data `delorean` will keep that offset as a ``pytz.FixedOffset`` timezone, if there is no timezone information passed in UTC is assumed.


Ambiguous cases
"""""""""""""""

There might be cases where the string passed to parse is a bit ambiguous for example. In the case where `2013-05-06` is passed is this May 6th, 2013 or is June 5th, 2013?

`Delorean` makes the assumptions that ``dayfirst=True`` and ``yearfirst=True`` this will lead to the following precedence.


    If dayfirst is True and yearfirst is True:

    - YY-MM-DD
    - DD-MM-YY
    - MM-DD-YY

So for example with default parameters `Delorean` will return '2013-05-06' as May 6th, 2013.

.. doctest::

    >>> parse("2013-05-06")
    Delorean(datetime=datetime.datetime(2013, 5, 6, 0, 0), timezone='UTC')

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

.. doctest::

    >>> import delorean
    >>> from delorean import stops
    >>> for stop in stops(freq=delorean.HOURLY, count=10, start=datetime(2013, 1, 21, 6, 25, 33)):
    ...     print(stop)
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

.. doctest::

    >>> import delorean
    >>> from delorean import stops
    >>> from datetime import datetime
    >>> d1 = datetime(2012, 5, 6)
    >>> d2 = datetime(2013, 5, 6)

.. note::

   The ``stops`` method only accepts naive datetime ``start`` and ``stop`` values.

Now in the case where you provide `timezone`, `start`, and `stop` all is good in the world!

.. doctest::

    >>> for stop in stops(freq=delorean.DAILY, count=10, timezone="US/Eastern", start=d1, stop=d2):
    ...     print(stop)
    Delorean(datetime=datetime.datetime(2012, 5, 6, 0, 0), timezone='US/Eastern')
    Delorean(datetime=datetime.datetime(2012, 5, 7, 0, 0), timezone='US/Eastern')
    Delorean(datetime=datetime.datetime(2012, 5, 8, 0, 0), timezone='US/Eastern')
    Delorean(datetime=datetime.datetime(2012, 5, 9, 0, 0), timezone='US/Eastern')
    Delorean(datetime=datetime.datetime(2012, 5, 10, 0, 0), timezone='US/Eastern')
    Delorean(datetime=datetime.datetime(2012, 5, 11, 0, 0), timezone='US/Eastern')
    Delorean(datetime=datetime.datetime(2012, 5, 12, 0, 0), timezone='US/Eastern')
    Delorean(datetime=datetime.datetime(2012, 5, 13, 0, 0), timezone='US/Eastern')
    Delorean(datetime=datetime.datetime(2012, 5, 14, 0, 0), timezone='US/Eastern')
    Delorean(datetime=datetime.datetime(2012, 5, 15, 0, 0), timezone='US/Eastern')


.. note::

   if no ``start`` or ``timezone`` value is specified start is assumed to be localized UTC object. If timezone is provided
   a normalized UTC to the correct timezone.

Now in the case where a naive stop value is provided you can see why the follow error occurs if you take into account the above note.

.. doctest::

    >>> for stop in stops(freq=delorean.DAILY, timezone="US/Eastern", stop=d2):
    ...     print(stop)
    Traceback (most recent call last):
        ...
    ValueError: RRULE UNTIL values must be specified in UTC when DTSTART is timezone-aware

You will be better off in scenarios of this nature to skip using either and use count to limit the range of the values returned.

.. doctest::
    :options: +ELLIPSIS

    >>> from delorean import stops
    >>> for stop in stops(freq=delorean.DAILY, count=2, timezone="US/Eastern"):
    ...     print(stop)
    Delorean(datetime=datetime.datetime(...), timezone='US/Eastern')
    Delorean(datetime=datetime.datetime(...), timezone='US/Eastern')
