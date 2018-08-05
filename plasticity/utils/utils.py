from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from functools import reduce


def deep_get(dictionary, *keys):
    """Deeply gets a key sequence from a dictionary.

    Gets a key sequence from a nested dictionary or returns `None` if the
    key sequence doesn't exist.
    :param dictionary: The dictionary to get from
    :type dictionary: dict
    :param *keys: The key sequence to get (e.g. 'foo', 'bar')
    :type *keys: str
    :returns: The value at the key sequence or `None`
    :rtype: {any}
    """
    return reduce(lambda d, key: d.get(key, None) if isinstance(d, dict)
                  else None, keys, dictionary)
