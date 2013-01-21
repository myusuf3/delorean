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

Now lets create a create `datetime` with the current datetime and UTC timezone::

    >>> d = Delorean()
    >>> d
    Delorean(datetime=2013-01-12 06:10:33.110674+00:00,  timezone=UTC)

Do you want to normalize this timezone to another timezone? Simply do the following::

   >>> d = d.shift("US/Eastern")
   >>> d
   Delorean(datetime=2013-01-12 01:10:38.102223-05:00, timezone=US/Eastern)

Now that you have successfully shifted the timezone you can easily return a localized datetime object or date with ease.::

    >>> d.datetime
    datetime.datetime(2013, 1, 12, 01, 10, 38, 102223, tzinfo=<DstTzInfo 'US/Eastern' EST-1 day, 19:00:00 STD>)
    >>> d.date
    datetime.date(2013, 1, 12)

For the purists out there you can do things like so::

    >>> d.naive()
    datetime.datetime(2013, 1, 12, 1, 10, 38, 102223)
    >>> d.epoch()
    1357971038.102223

You can also create Delorean object using unix timestamps.::

    from delorean import epoch
    >>> epoch(1357971038.102223).shift("US/Eastern")
    Delorean(datetime=2013-01-12 01:10:38.102223-05:00, timezone=US/Eastern)

As you can see `delorean` return a Delorean object which you can shift to appropriate timezone to get back your original datetime object from above.

Natural Language
^^^^^^^^^^^^^^^^
`Delorean` provides many ways to get certain date relative to one another, often time to get something simple a next year or the next thursday can be quite troublesome.

`Delorean` provides several conveniences for this type of behaviour. For example if you wanted to get next Tuesday from today you would simple do the following::

    >>> d = Delorean()
    >>> d
    Delorean(datetime=2013-01-20 19:41:06.207481+00:00, timezone=UTC)
    >>> d.next_tuesday()
    Delorean(datetime=2013-01-22 19:41:06.207481+00:00, timezone=UTC)

Last Tuesday? Two Tuesdays ago at midnight? No problem.::

    >>> d.last_tuesday()
    Delorean(datetime=2013-01-15 19:41:06.207481+00:00, timezone=UTC)
    >>> d.last_tuesday(2).midnight()
    datetime.datetime(2013, 1, 8, 0, 0, tzinfo=<UTC>)

Truncation
^^^^^^^^^^
Often times we dont care how many milliseconds or even seconds that present in our datetime object. It often becomes a nuisance to retrieve `datetimes` that for example occur in the same minute. You would have to through the annoying process of replacing zero for the units you don't care for then doing a comparison.

`Delorean` comes with a method that allows you to easily truncate to different unit of time milliseconds, second, minute, hour, etc.::

    >>> d = Delorean()
    >>> d
    Delorean(datetime=2013-01-21 03:34:30.418069+00:00, timezone=UTC)
    >>> d.truncate('second')
    Delorean(datetime=2013-01-21 03:34:30+00:00, timezone=UTC)
    >>> d.truncate('hour')
    Delorean(datetime=2013-01-21 03:00:00+00:00, timezone=UTC)

Those might seem obvious `delorean` also provides truncation to the month and year levels as well.::

    >>> d = Delorean(datetime=datetime(2012, 05, 15, 03, 50, 00, 555555), timezone="US/Eastern")
    >>> d
    Delorean(datetime=2012-05-15 03:50:00.555555-04:00, timezone=US/Eastern)
    >>> d.truncate('month')
    Delorean(datetime=2012-05-01 00:00:00-04:00, timezone=US/Eastern)
    >>> d.truncate('year')
    Delorean(datetime=2012-01-01 00:00:00-04:00, timezone=US/Eastern)

Strings and Parsing
^^^^^^^^^^^^^^^^^^^
Another pain dealing with strings of datetimes. `Delorean` can help you parse all those annoying strings you get from various APIs.::

    >>> from delorean import parse
    >>> parse("2011/01/01 00:00:00 -0700")
    Delorean(datetime=2011-01-01 07:00:00+00:00, timezone=UTC)

As shown above if the string passed has offset data `delorean` will convert the resulting object to UTC, if there is no timezone information passed in UTC is assumed.

Making A Few Stops
^^^^^^^^^^^^^^^^^^
Delorean wouldn't be complete without making a few stop in all the right places.::

    >>> from delorean import stops
    >>> from delorean import HOURLY
    >>> for stop in stops(freq=HOURLY, count=10):    print stop
    ...
    Delorean(datetime=2013-01-21 06:25:33+00:00, timezone=UTC)
    Delorean(datetime=2013-01-21 07:25:33+00:00, timezone=UTC)
    Delorean(datetime=2013-01-21 08:25:33+00:00, timezone=UTC)
    Delorean(datetime=2013-01-21 09:25:33+00:00, timezone=UTC)
    Delorean(datetime=2013-01-21 10:25:33+00:00, timezone=UTC)
    Delorean(datetime=2013-01-21 11:25:33+00:00, timezone=UTC)
    Delorean(datetime=2013-01-21 12:25:33+00:00, timezone=UTC)
    Delorean(datetime=2013-01-21 13:25:33+00:00, timezone=UTC)
    Delorean(datetime=2013-01-21 14:25:33+00:00, timezone=UTC)
    Delorean(datetime=2013-01-21 15:25:33+00:00, timezone=UTC)

This allows you to do clever composition like daily, hourly, etc. This method is a generator that produces `Delorean` objects. Excellent for things like getting every Tuesday for the next 10 weeks, or every other hour for the next three months.
