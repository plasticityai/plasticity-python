from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


class Service(object):
    """An Service is one of the main APIs, such as Sapien or Cortex.

    Attributes:
        plasticity: a Plasticity instance with the API URL and token
    """

    def __init__(self, plasticity):
        """Initializes a new Service."""
        self.plasticity = plasticity
