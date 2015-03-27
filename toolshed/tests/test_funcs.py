from toolshed.compatibility import update_wrapper, wraps
from toolshed.funcs import unwrap

def stopdeco(f):
    @wraps(f)
    def wrapper(*a, **k):
        return f(*a, **k)
    wrapper.__stops__ = True
    return wrapper

def test_unwrap():
    my_func = lambda x, y: x+y
    my_wrapper = update_wrapper(lambda f, *a: f(*a), my_func)
    assert unwrap(my_wrapper) is my_func

def test_unwrap_with_stop():
    def myfunc():
        pass

    stop = lambda f: getattr(f, '__stops__', False)

    assert unwrap(stopdeco(myfunc), stop) is not myfunc
