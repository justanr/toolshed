from functools import partial, WRAPPER_ASSIGNMENTS, WRAPPER_UPDATES
from toolz.compatibility import *
from toolz.compatibility import __all__ as compat_all

__all__ = compat_all + ('update_wrapper', 'wraps')

# pending removal based on acceptance of toolz pull request 230
# see: https://github.com/pytoolz/toolz/pull/230
def update_wrapper(wrapper, wrapped, 
                   assigned=WRAPPER_ASSIGNMENTS,
                   updated=WRAPPER_UPDATES):
    """Makes a wrapping object appear and act like the underlying wrapped
    object.

    This is a backport of Python 3.4's update_wrapper which has much smarter
    behavior than the update_wrapper that exists in prior versions as it
    uses a try/except/else block rather than charitably assuming all items
    exist on the wrapped object (functools.partial has no `__name__` attribute
    for example).

    It also backports the `__wrapped__` attribute for easy access to the 
    original object.

    WARNING!!: This function modifies the wrapping object!

    This is more useful for class based wrappers, for function wrappers see
    ``wraps`` below.

    >>> class Decorator(object):
    ...     "Wraps a function in a callable object."
    ...     def __init__(self, f):
    ...         update_wrapper(self, f)
    ...         self.f = f
    ...     def __call__(self, *args, **kwargs):
    ...         return self.f(*args, **kwargs)

    >>> @Decorator
    ... def add(x, y):
    ...     "Adds two objects."
    ...     return x + y

    >>> print(add.__name__)
    add
    >>> print(add.__doc__)
    Adds two objects
    """
    for attr in assigned:
        try:
            value = getattr(wrapped, attr)
        except AttributeError:
            pass
        else:
            setattr(wrapper, attr, value)

    for attr in updated:
        getattr(wrapper, attr, {}).update(getattr(wrapped, attr, {}))

    # store original callable last so it isn't accidentally copied over
    # in event of wrapping multiple times
    wrapper.__wrapped__ = wrapped

    return wrapper

def wraps(wrapped, assigned=WRAPPER_ASSIGNMENTS, updated=WRAPPER_UPDATES):
    """Decorator form of ``update_wrapper``.

    This is very useful for writing closure based decorators
    rather than manually using ``update_wrapper`` on the closure.

    WARNING!!: This function modifies the function it is applied to!
    """
    return partial(update_wrapper, wrapped=wrapped,     #noqa
                   assigned=assigned, updated=updated)  #noqa
