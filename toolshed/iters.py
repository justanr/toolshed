from collections import namedtuple
from toolz import itertoolz

__all__ = ('grange',)

_Grange = namedtuple('_Grange', ['start', 'stop', 'step', 'has_neg_step'])

class grange(_Grange):
    """A generalized range class that allows creating ranges of arbitrary
    types such as dates, floats, etc.

    If only start and step provided, grange will create an infinite stream
    of objects that decrement/increment based on step.
   
    Objects to grange over must be orderable and support addition. If the
    objects support modulo with the checked value, a fast-path contains 
    will be taken, otherwise an `x in iter(self)` path is taken.

    Be careful with `x in grange(start, step)` as with any other infinite
    sequence.

    >>> from datetime import datetime, timedelta
    >>> begin = datetime(2015, 3, 1)
    >>> end = datetime(2015, 3, 8)
    >>> step = timedelta(days=2)
    >>> drange = grange(begin, end, step)
    >>> list(drange)
    [datetime.datetime(2015, 3, 1, 0, 0),
     datetime.datetime(2015, 3, 3, 0, 0),
     datetime.datetime(2015, 3, 5, 0, 0)]
    """ 
    # use __new__ when inheriting from tuple rather than __init__
    def __new__(self, start=None, stop=None, step=None):
        if step is None:
            raise TypeError("must provide step for grange.")
        if start is None: 
            raise TypeError("must provide starting point for grange.")

        # since this deals with arbitrary objects
        # it's unlikely step < 0 will work
        has_neg_step = (start + step) < start
      
        # explicitly invoke parent __new__ rather than super().__new__
        # which hits object.__new__
        return _Grange.__new__(self, start, stop, step, has_neg_step)

    def __repr__(self):
        return "{!s}(start={!r}, stop={!r}, step={!r}".format(  #noqa
                self.__class__.__name__,  #noqa
                self.start,  #noqa
                self.stop,   #noqa
                self.step)   #noqa

    def __len__(self):
        if self.stop is None:
            # it'd be nice if float('inf') could be returned
            raise TypeError("infinite range") 
        try:
            if self.has_neg_step:
                calc = (self.start - self.stop + self.step + 1)
            else:
                calc = (self.stop - self.start + self.step - 1)
            return max(0, calc//self.step)
        except TypeError:
            # likely due to arthimetic error
            # or non-comparable types in max
            # this is possibly unsafe behavior
            return len(list(iter(self)))

    def _check_stop(self, current):
        """In keeping with __builtin__.range's behavior,
        if the current value is one step away (or less) from the stopping
        point, then we should terminate the iteration.

        This is a helper method to determine when that point it.

        >>> grange(0, 6, 2)._check_stop(4)
        ... True
        """
        stop = self.stop - self.step
        if self.has_neg_step:
            return current <= stop
        return current >= stop

    def __contains__(self, x):
        """Checks if a value exists in the range. This attempts to take
        the fastest path by and attempts to emulate __builtin__.range

        If there's no stopping point, there's a real possibility this check
        will fall into an infinite loop.

        >>> from datetime import datetime, timedelta
        >>> start, stop = datetime(2015, 3, 1), datetime(2015, 3, 7)
        >>> step = timedelta(days=2)
        >>> drange = grange(start, stop, step)
        >>> assert datetime(2015, 3, 3) in drange
        """
        if self.stop is not None:
            if self.has_neg_step:
                check = x <= self.start and x > self.stop
            else:
                check = x >= self.start and x < self.stop

            # out of range
            if not check:
                return False

            try:
                return not x % self.step
            # likely an illegal operation 
            # or x was checked for `__mod__` explicitly
            except (TypeError, AttributeError):
                pass
        
        # fall off to here because there's no stopping point
        # x doesn't have the `%` operator defined or x % step 
        # raised a TypeError.
        return x in iter(self)


    def __iter__(self):
        current = self.start
        stopping = self.stop is not None

        while True:
            if stopping and self._check_stop(current): 
                break
            yield current
            current = current + self.step

