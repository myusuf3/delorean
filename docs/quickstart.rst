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
    Delorean(datetime=2013-01-08 19:41:06.207481+00:00, timezone=UTC)

Truncation
^^^^^^^^^^
Often times we dont care how many milliseconds or even seconds that present in our datetime object. It often becomes a nuisance to compare `datetimes` that for example occur in the same day or even in the same month.




Timezones
^^^^^^^^^


Datetimes and Dates
^^^^^^^^^^^^^^^^^^^

Exceptions
^^^^^^^^^^
