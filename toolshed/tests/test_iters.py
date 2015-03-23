from datetime import datetime, timedelta
from nose.tools import assert_raises
from toolshed.iters import (grange, unzip)

# helpers
def make_drange(neg=False):
    start = datetime(2015, 3, 1)
    stop = datetime(2015, 3, 8)
    step = timedelta(days=(2 if not neg else -2))
    return grange(start, stop, step)


# actual tests
def test_unzip():
    assert [('tim', 'sam'), (1,2)] == list(unzip(('tim', 1), ('sam', 2)))

def test_grange_has_neg_step():
    assert grange(4, 1, -1)._has_neg_step
    assert make_drange(True)._has_neg_step


def test_grange_len():
    assert len(grange(0, 4, 1)) == len(range(0, 4, 1))
    assert len(make_drange()) == len(list(make_drange()))
    assert len(grange(9, 55, 7)) == len(range(9, 55, 7))


def test_grange_in():
    assert datetime(2015, 3, 3) in make_drange()


def test_len_grange_raises_with_inf():
    assert_raises(TypeError, len, grange(1, step=1))


def test_grange_check_stop():
    irange = grange(0,6,2)
    neg_irange = grange(6, 0, -2)
    assert irange._check_stop(6)
    assert neg_irange._check_stop(0)


def test_grange_builds_length():
    drange = make_drange()
    assert drange._length is None
    len(drange)
    assert drange._length
