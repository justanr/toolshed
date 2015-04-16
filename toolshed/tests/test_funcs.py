from functools import WRAPPER_ASSIGNMENTS
from toolshed.compatibility import update_wrapper, wraps
from toolshed.funcs import *

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


def test_kwargs_deco_looks_like_wrapped():
    def my_kw_deco(func, thing):
        "a doc string"
        return func

    wrapped = kwargs_decorator(my_kw_deco)
    assert hasattr(wrapped, '__wrapped__') and wrapped.__wrapped__ is my_kw_deco
    assert all(getattr(my_kw_deco, attr) == getattr(wrapped, attr)
               for attr in WRAPPER_ASSIGNMENTS)


def test_kwargs_deco_works():
    @kwargs_decorator
    def my_deco(func, thing):
        func.thing = thing
        return func

    @my_deco(thing=True)
    def stub():
        pass

    assert stub.thing


def test_kwargs_deco_with_defaults():
    @kwargs_decorator
    def my_kw_deco(func, thing=True):
        func.thing = thing
        return func

    @my_kw_deco
    def stub():
        pass

    assert stub.thing


def test_kwargs_deco_on_class():
    class W(object):
        def __init__(self, f, thing):
            update_warpper(self, f)
            self.thing = thing
            self.f = f

        def __call__(self, *a, **k):
            return self.f(*a, **k)

    wrapped_w = kwargs_decorator(W)

    assert wrapped_w.__wrapped__ is W
    assert all(getattr(W, attr) == getattr(wrapped_w, attr)
               # classes don't have the __annotations__ attr by default
               for attr in WRAPPER_ASSIGNMENTS if attr != '__annotations__')
