from functools import partial
from .compatibility import wraps

__all__ = ('unwrap', 'kwargs_decorator')

def unwrap(func, stop=None):
    """Backport of Python 3.4's inspect.unwrap function.

    Retrieves the object wrapped by func, following the chain of __wrapped__
    attributes to reach the originally wrapped object.

    Allows an optional stop callback which accepts the *current* function
    as its only argument that will allow unwrapping to stop early if it
    returns True.

    Raises ValueError if a cycle is encountered.

    If Python <3.3, use ``toolshed.update_wrapper`` and ``toolshed.wraps``
    to emulate behavior expected here.

    >>> my_func = lambda x,y: x+y
    >>> my_wrapper = update_wrapper(lambda *a: my_func(*a), my_func)
    >>> f = toolshed.update_wrapper()
    >>> unwrap(f) is my_func
    ... True
    """

    if stop is None:
        _is_wrapper = lambda f: hasattr(f, '__wrapped__')
    else:
        _is_wrapper = lambda f: hasattr(f, '__wrapped__') and not stop(f)

    # remember original function for error reporting
    f = func
    # memoize by id(f) to tolerate non hashable objects
    memo = {id(func)}

    while _is_wrapper(func):
        func = func.__wrapped__
        id_func = id(func)
        if id_func in memo:
            raise ValueError("wrapper loop when unwrapping {!r}".format(f))
        memo.add(id_func)
    return func


def kwargs_decorator(deco):
    """A decorator to help create decorators that accept keyword arguments.
    It's a relatively simple trick of checking in the closure if it's
    received the func parameter. If not, a partial with all the current
    keywords is returned. Otherwise, the decorator is run with the provided
    function and keyword arguments.

    >>> @kwargs_decorator
    ... def my_kwarg_deco(f, pre, post):
    ...     @wraps(f)
    ...     def wrapper(*a, **k):
    ...         print(pre)
    ...         res = f(*a, **k)
    ...         print(post)
    ...         return res
    ...     return wrapper

    Using this new decorator is similar to using any other, except keyword
    arguments can be passed:

    >>> @my_kwargs_deco(pre='Hello!', post='Goodbye!')
    ... def say_name(name):
    ...     print(name)

    Something else that is nice, is that if default values are provided to
    the decorator, it can be used just like a regular decorator -- that is,
    without the explicit invocation.

    >>> @kwargs_decorator
    ... def deco_with_defaults(f, pre='hello', post='goodbye'):
    ...     @wraps(f)
    ...     def wrapper(*a, **k):
    ...         print(pre)
    ...         res = f(*a, **k)
    ...         print(post)
    ...         return res
    ...     return wrapper
    ...
    >>> @deco_with_defaults
    ... def say_name(name):
    ...     print(name)

    It should be noted that the created decorator isn't really reentrant, so
    stacking like this isn't possible:

    >>> @my_kwarg_deco(pre='hello')
    ... @my_kwarg_deco(post='goodbye')
    ... def my_cool_func():
    ...     return None

    This decorator can also be used on classes as well (which requires 2.6+):

    >>> @kwarg_decorator
    ... class pre_post_print(object):
    ...     def __init__(self, f, pre='', post=''):
    ..          self.f = f
    ...         self.pre = pre
    ...         self.post = post
    ...
    ...     def __call__(self, *a, **k):
    ...         print(self.pre)
    ...         r = self.f(*a, **k)
    ...         print(self.post)
    ...         return r
    """
    @wraps(deco)
    def partialler(func=None, **kwargs):
        if func is None:
            return partial(partialler, **kwargs)
        else:
            return deco(func, **kwargs)
    return partialler
