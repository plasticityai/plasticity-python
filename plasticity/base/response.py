from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


class Response(object):
    """A Response is a specific API response to an API endpoint.

    Attributes:
        plasticity: a Plasticity instance with the API URL and token
    """
    def __init__(
            self, data, error, error_code, error_message,
            graph_enabled=None, ner_enabled=None, pretty_enabled=None):
        self.data = data
        self.error = error
        self.error_code = error_code
        self.error_message = error_message

        self.graph_enabled = graph_enabled
        self.ner_enabled = ner_enabled
        self.pretty_enabled = pretty_enabled

    def __repr__(self):
        return '<Response {}>'.format(id(self))

    def __str__(self):
        return '<Response {}>'.format(id(self))

    @classmethod
    def from_json(cls, res, **kwargs):
        """Builds a `Response` from a json object."""
        data = res.get('data')
        error = res.get('error')
        error_code = res.get('errorCode')
        error_message = res.get('message')
        return cls(data, error, error_code, error_message, **kwargs)
