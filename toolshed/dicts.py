import toolz
from .compatibility import (iterkeys, itervalues, iteritems, zip)

__all__ = ('invert', 'invert_with', 'split_keys_values', 'sorted_items')

def invert(d):
    """Inverts a dictionary from key->value mapping to a
    value->key mapping. The values being switched to keys must be hashable.

    >>> invert({'ashley': 6, 'timothy': 15})
    ... {6: 'ashley', 15: 'timothy'}
    """
    return dict(toolz.itemmap(reversed, d))

def invert_with(f, d):
    """Inverts a dictionary from key->value mapping to a
    value->key mapping with some transform on the old values.
    The new keys must be hashable, per dictionary requirements.

    The transforming function needs to accept only the value as an
    argument.

    >>> invert_with(sum, {'ashley': [1,2,3], 'timothy': [4,5,6]})
    ... {6: 'ashley', 15: 'timothy'}
    """
    r_f = lambda item: (f(item[1]), item[0])
    return dict(toolz.itemmap(r_f, d))

def split_keys_values(d):
    """Breaks a dictionary's item tuples into tuples of keys and list.

    Equivalent to doing: `keys, values = iterkeys(d), itervalues(d)`

    >>> list(split_keys_values({'ashley': 6, 'timothy': 15}))
    ... [('ashley', 'timothy'), (6, 15)]
    """
    return zip(*iteritems(d))

def sorted_items(key, d, reverse=False):
    """Sorts a dictionary's items based on some key function. The key
    function needs to accept the full item tuple of `(k, v)` but may
    sort based on any aspect of it.

    >>> {'ashley': 6, 'sam': 20, 'tim': 15}
    >>> list(sorted_items(itemgetter(1), d))
    ... [('ashley', 6), ('tim', 15), ('same', 20)]
    """
    return sorted(iteritems(d), key=key, reverse=reverse)
