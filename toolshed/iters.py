from __future__ import division
from math import ceil
from .compatibility import zip

__all__ = ('grange',)


def unzip(*groups):
    """Alias for zip(*groups).

    Used to unzip pairs based on their items.

    >>> u = unzip(toolz.compatiblity.iteritems({'ashley': 6, 'timothy': 15}))
    >>> list(u)
    ... [('ashley', 'timothy'), (6, 15)]
    """
    return zip(*groups)


class grange(object):
    """A generalized range class that allows creating ranges of arbitrary
    types such as dates, floats, etc.

    If only start and step provided, grange will create an infinite stream
    of objects that decrement/increment based on step.

    >>> from datetime import datetime, timedelta
    >>> begin, end = datetime(2015, 3, 1), datetime(2015, 3, 8)
    >>> step = timedelta(days=2)
    >>> list(grange(begin, end, step))
    ... [datetime.datetime(2015, 3, 1, 0, 0),
    ...  datetime.datetime(2015, 3, 3, 0, 0),
    ...  datetime.datetime(2015, 3, 5, 0, 0)]

    There are a few restrictions:

    - Objects must be orderable and support __add__ and __sub__
    - `start + step` must return an object that fulfills these restrictions

    It's fair to say that the internals of grange (start, stop, step)
    shouldn't be poked at. Short of abusing inheritance from tuple or
    overwritting `__setattr__`, there's no easy way to do this in pure Python.
    """
    def __init__(self, start=None, stop=None, step=None):
        if step is None:
            raise TypeError("must provide step for grange.")
        if start is None: 
            raise TypeError("must provide starting point for grange.")

        self._start = start
        self._stop = stop
        self._step = step

        # for caching length once requested
        # grange.__len__ is potentially O(n)
        self._length = None

        # since this deals with arbitrary objects
        # it's unlikely step < 0 will work
        self._has_neg_step = (start + step) < start

    @property
    def start(self):
        return self._start

    @property
    def stop(self):
        return self._stop

    @property
    def step(self):
        return self._step

    def __repr__(self):
        return "{!s}(start={!r}, stop={!r}, step={!r}".format(  #noqa
                self.__class__.__name__,  #noqa
                self.start,  #noqa
                self.stop,   #noqa
                self.step)   #noqa

    def __len__(self):
        """Attempt to calculate the length of a grange.

        If this is an infinite sequence, a TypeError is raised -- only
        because `__len__` must return an integer and INF is a float.

        Otherwise, this attempts to calculate the length intelligently.
        If that's not possible, for some reason, a Hail Mary is thrown
        and the length of the list built from ``grange.__iter__``.

        After a length is calculated, it's cached since grange's internals
        shouldn't be poked at.
        """
        if self.stop is None:
            # it'd be nice if float('inf') could be returned
            raise TypeError("infinite range")

        if self._length:
            return self._length

        try:
            if self._has_neg_step:
                calc = self.start - self.stop
            else:
                calc = self.stop - self.start
            # ew.
            length = int(ceil(abs(calc/self.step)))
        except TypeError:
            # likely due to arthimetic error
            # this is possibly unsafe behavior
            length = len(list(iter(self)))

        self._length = length
        return length

    # ???: memoize?
    def __contains__(self, x):
        """Checks if a value exists in the range. This attempts to take
        the fastest path by and attempts to emulate __builtin__.range

        This happens by checking if the value is within the bounds of
        the grange then attempting to modulo the value with the step.
        The second step works *fantastic* for integers, but with arbirtary
        objects, maybe not so much.

        If the modulo operation throws a TypeError or AttributeError,
        then a hail mary is thrown and the grange is iterized and an
        in check is done against that. There's a real possibility this check
        will fall into an infinite loop if there's no stopping point.

        >>> from datetime import datetime, timedelta
        >>> start, stop = datetime(2015, 3, 1), datetime(2015, 3, 8)
        >>> step = timedelta(days=2)
        >>> assert datetime(2015, 3, 3) in grange(start, stop, step)
        """
        if self.stop is not None:
            if self._has_neg_step:
                check = self.start >= x > self.stop
            else:
                check = self.start <= x < self.stop
        else:
            if self._has_neg_step:
                check = self.start >= x
            else:
                check = self.start <= x

        if not check:
            return False

        try:
            # attempt to emulate __builtin__.range fast path
            return not x % self.step
        # likely an illegal operation
        # or x was checked for `__mod__` explicitly
        except (TypeError, AttributeError):
            pass

        # fall off to here because there's no stopping point
        # x doesn't have the `%` operator defined or x % step 
        # raised a TypeError.
        return x in iter(self)

    def _check_stop(self, current):
        """In keeping with __builtin__.range's behavior,
        if the current value is one step away (or less) from the stopping
        point, then we should terminate the iteration.

        This is a helper method to determine when that point it.
        >>> grange(0, 6, 2)._check_stop(4)
        ... True
        """
        if self._has_neg_step:
            return current <= self.stop
        return current >= self.stop

    def __iter__(self):
        """Generates members of the range until the stopping point
        is reached.
        """
        current = self.start
        stopping = self.stop is not None

        while True:
            if stopping and self._check_stop(current): 
                break
            yield current
            current = current + self.step

