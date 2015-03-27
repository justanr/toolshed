__all__ = ('unwrap',)

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
