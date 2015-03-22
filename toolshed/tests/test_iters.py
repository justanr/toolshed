from datetime import datetime, timedelta

from nose.tools import assert_raises
from toolshed.iters import (grange)

def make_drange(neg=False):
    start = datetime(2015, 3, 1)
    stop = datetime(2015, 3, 8)
    step = timedelta(days=(2 if not neg else -2))
    return grange(start, stop, step)

def test_grange_has_neg_step():
    assert grange(4, 1, -1).has_neg_step
    assert make_drange(True).has_neg_step

def test_grange_len():
    assert len(grange(0, 4, 1)) == 4
    assert len(make_drange()) == 3

def test_grange_in():
    assert datetime(2015, 3, 3) in make_drange()

def test_len_grange_raises_with_inf():
    assert_raises(TypeError, len, grange(1, step=1))

def test_grange_check_stop():
    irange = grange(0,6,2)
    assert irange._check_stop(4)
