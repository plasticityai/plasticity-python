from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from plasticity.base.service import Service


class Cortex(Service):
    """Cortex is the API service for knowledge. Its functions are described 
    here: https://www.plasticity.ai/api/docs/#cortex
    """

    def __init__(self, plasticity):
        """Initializes a new Cortex Service."""
        super(Cortex, self).__init__(plasticity)
        self.url = self.plasticity.url + "cortex/"
