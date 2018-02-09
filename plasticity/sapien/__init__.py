from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from plasticity.base.service import Service


class Sapien(Service):
    """Sapien is the API service for language. Its functions are 
    described here: https://www.plasticity.ai/api/docs/#sapien
    """

    def __init__(self, plasticity):
        """Initializes a new Sapien Service."""
        super(Sapien, self).__init__(plasticity)
        self.url = self.plasticity.url + "sapien/"

        # Endpoints
        self._core = None
        self._names = None

    @property
    def core(self):
        if self._core is None:
            from plasticity.sapien.core import Core
            self._core = Core(self.plasticity)
        return self._core

    @property
    def names(self):
        if self._names is None:
            from plasticity.sapien.names import Names
            self._names = Names(self.plasticity)
        return self._names
