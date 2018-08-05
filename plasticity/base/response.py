from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from plasticity.utils import utils


class Response(object):
    """A Response is a specific API response to an API endpoint.

    Attributes:
        plasticity: a Plasticity instance with the API URL and token
    """
    def __init__(
            self, data, error, graph_enabled=None, ner_enabled=None,
            pretty_enabled=None):
        self.data = data
        self.error = error

        self.graph_enabled = graph_enabled
        self.ner_enabled = ner_enabled
        self.pretty_enabled = pretty_enabled

    def __repr__(self):
        return '<Response %s>' % id(self)

    def __str__(self):
        return '<Response %s>' % id(self)

    @classmethod
    def from_json(cls, res, **kwargs):
        """Builds a `Response` from a json object."""
        data = utils.deep_get(res, 'data')
        error = utils.deep_get(res, 'error')
        return cls(data, error, **kwargs)
