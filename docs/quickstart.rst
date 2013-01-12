Quickstart
===========
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
    <Delorean[ 2013-01-12 06:10:33.110674+00:00  UTC ]>

Do you want to normalize this timezone to another timezone? Simply do the following::

   >>> d.shift("US/Eastern")
   <Delorean[ 2013-01-12 01:10:38.102223-05:00  US/Eastern ]>



Timezones
^^^^^^^^^


Datetimes and Dates
^^^^^^^^^^^^^^^^^^^

Exceptions
^^^^^^^^^^
