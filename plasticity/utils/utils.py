from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


def key_defined_and_has_value(dictionary, *keys):
    return True if deep_get(dictionary, *keys) else False

def deep_get(dictionary, *keys):
    return reduce(lambda d, key: d.get(key, None) if isinstance(d, dict) 
        else None, keys, dictionary)
