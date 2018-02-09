from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import requests

from plasticity.utils import utils
from plasticity.base.endpoint import Endpoint


class Names(Endpoint):
    """The Names Endpoint performs all the Names API functions 
    described here: https://www.plasticity.ai/api/docs/#sapien-names
    """

    def __init__(self, plasticity):
        """Initializes a new Names Endpoint."""
        super(Names, self).__init__(plasticity)
        self.url = self.plasticity.sapien.url + "names/"

    def post(self, name, pretty=False):
        payload = json.dumps({
            'name': name,
            'pretty': pretty
        })
        return self.plasticity._post(self._url, data)

    def is_male_name(self, name):
        res = self.post(name)
        is_male = utils.deep_get(res, 'data', 'isMaleName', 'value')
        is_certain = utils.deep_get(
            res, 'data', 'isMaleName', 'confidence') == 'Certain'
        return is_male and is_certain

    def is_female_name(self, name):
        res = self.post(name)
        is_female = utils.deep_get(res, 'data', 'isFemaleName', 'value')
        is_certain = utils.deep_get(
            res, 'data', 'isFemaleName', 'confidence') == 'Certain'
        return is_female and is_certain

    def is_first_name(self, name):
        res = self.post(name)
        is_male = utils.deep_get(res, 'data', 'isMaleName', 'value')
        is_m_certain = utils.deep_get(
            res, 'data', 'isMaleName', 'confidence') == 'Certain'
        is_female = utils.deep_get(res, 'data', 'isFemaleName', 'value')
        is_f_certain = utils.deep_get(
            res, 'data', 'isFemaleName', 'confidence') == 'Certain'
        return (is_male and is_m_certain) or (is_female and is_f_certain)

    def is_family_name(self, name):
        res = self.post(name)
        is_family_name = utils.deep_get(res, 'data', 'isFamilyName', 'value')
        is_certain = utils.deep_get(
            res, 'data', 'isFamilyName', 'confidence') == 'Certain'
        return is_family_name and is_certain

    def is_name(self, name):
        res = self.post(name)
        is_name = utils.deep_get(res, 'data', 'isName', 'value')
        is_certain = utils.deep_get(
            res, 'data', 'isName', 'confidence') == 'Certain'
        return is_name and is_certain
