from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import textwrap
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
    return reduce(lambda d, key:
                  d.get(key, None) if isinstance(d, dict) else None,
                  keys, dictionary)


def indent(text, prefix='\t'):
    """Indents text with some prefix.

    Indents text with some prefix using textwrap (if Python > 3.3)
    or a custom method.
    :param text: The text to indent
    :type text: str
    :param prefix: The prefix to indent with, defaults to '\t'
    :type prefix: str, optional
    :returns: The indented text by prefix
    :rtype: {str}
    """
    try:
        textwrap.indent
    except AttributeError:  # function wasn't added until Python 3.3
        return ''.join(prefix+line for line in text.splitlines(True))
    else:
        return textwrap.indent(text, prefix)


def fill(text, width=70):
    """Wraps text to a max length of width.

    Shadow's the textwrap `fill()` function, which wraps the
    single paragraph in text, and returns a single string
    containing the wrapped paragraph.
    :param text: The text to fill
    :type text: str
    :param width: The max width, defaults to 70
    :type width: number, optional
    :returns: The filled text
    :rtype: {str}
    """
    return textwrap.fill(text, width=width)


def shorten(text, width=70, placeholder='...'):
    """Shortens text to a max length.

    Shortens text to a max length using some optional placeholder
    with textwrap (if Python > 3.3) or a custom method.
    :param text: The text to shorten
    :type text: str
    :param width: The max width, defaults to 70
    :type width: number, optional
    :param placeholder: The placeholder to truncate with, defaults to '...'
    :type placeholder: str, optional
    :returns: The shortened text with placeholder
    :rtype: {str}
    """
    try:
        textwrap.indent
    except AttributeError:  # function wasn't added until Python 3.3
        return (text
                if len(text) <= width
                else text[:width - len(placeholder)] + placeholder)
    else:
        return textwrap.shorten(text, width=width, placeholder=placeholder)
