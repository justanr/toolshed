from toolshed.dicts import (invert, invert_with, 
                            split_keys_values, sorted_items)

def test_invert():
    assert invert({'ashley': 6, 'timothy':15}) == {6: 'ashley', 15: 'timothy'}

def test_invert_with():
    in_ = {'ashley': [1,2,3], 'timothy': [4,5,6]}
    out = {6: 'ashley', 15: 'timothy'}

    assert invert_with(sum, in_) == out

def test_split_keys_values():
    d = {'ashley': 6, 'timothy': 15}
    k, v = split_keys_values(d)
    assert all(name in k for name in ['ashley', 'timothy'])
    assert all(num in v for num in [6, 15])
    assert all(d[k_] == v_ for k_, v_ in zip(k,v))

def test_sorted_items():
    d = {'ashley': 6, 'sam': 20, 'tim': 15}
    assert list(sorted_items(lambda i: i[1], d)) == \
           [('ashley', 6), ('tim', 15), ('sam', 20)]
