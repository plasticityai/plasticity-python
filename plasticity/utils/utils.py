from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


def deep_get(dictionary, *keys):
    """Deeply gets a key sequence from a dictionary."""
    return reduce(lambda d, key: d.get(key, None) if isinstance(d, dict)
                  else None, keys, dictionary)
