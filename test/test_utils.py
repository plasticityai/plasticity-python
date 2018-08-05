from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from plasticity.utils import utils


def test_deep_get_one_level():
    a = {'x': {'a': 1, 'b': '', 'c': {'d': '2'}}, 'y': 5}
    assert utils.deep_get(a, 'x') == {'a': 1, 'b': '', 'c': {'d': '2'}}
    assert utils.deep_get(a, 'y') == 5


def test_deep_get_two_levels():
    a = {'x': {'a': 1, 'b': '', 'c': {'d': '2'}}, 'y': 5}
    assert utils.deep_get(a, 'x', 'a') == 1
    assert utils.deep_get(a, 'x', 'b') == ''
    assert utils.deep_get(a, 'x', 'c') == {'d': '2'}


def test_deep_get_three_levels():
    a = {'x': {'a': 1, 'b': '', 'c': {'d': '2'}}, 'y': 5}
    assert utils.deep_get(a, 'x', 'c', 'd') == '2'


def test_deep_get_not_found():
    a = {'x': {'a': 1, 'b': '', 'c': {'d': '2'}}, 'y': 5}
    assert utils.deep_get(a, 'z') is None
    assert utils.deep_get(a, 'x', 'z') is None
