from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import json
import requests


class Plasticity(object):
    """A Plasticity class that holds the user's API token and 
    location (url) of the API to be used.

    Attributes:
        token: An API token to authenticate with the API
        url: A local or remote Plasticity API url to use
    """

    def __init__(self, token=None, url=None, environment=None):
        """Initializes a new Plasticity object."""
        environment = environment or os.environ
        self.url = url or 'https://api.plasticity.ai/'
        self.token = token or environment.get('PLASTICITY_API_KEY')

        # Services
        self._sapien = None
        self._cortex = None

    @property
    def sapien(self):
        if self._sapien is None:
            from plasticity.sapien import Sapien
            self._sapien = Sapien(self)
        return self._sapien

    @property
    def cortex(self):
        if self._cortex is None:
            from plasticity.cortex import Cortex
            self._cortex = Cortex(self)
        return self._cortex

    def _post(self, url, data):
        headers = {}
        headers['content-type'] = "application/json"
        if self.token:
            headers['authorization'] = "Bearer " + self.token
        response = requests.request("POST", url, data=data, headers=headers)
        return json.loads(response.text)
