from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


class Endpoint(object):
    """An Endpoint is a specific API action with in an API service.

    Attributes:
        plasticity: a Plasticity instance with the API URL and token
    """

    def __init__(self, plasticity):
        """Initializes a new Endpoint."""
        self.plasticity = plasticity
