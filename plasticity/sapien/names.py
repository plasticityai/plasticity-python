from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json

from plasticity.utils import utils
from plasticity.base.endpoint import Endpoint
from plasticity.base.response import Response


class Names(Endpoint):
    """The Names Endpoint performs all the Names API functions
    described here: https://www.plasticity.ai/api/docs/#sapien-names
    """
    def __init__(self, plasticity):
        """Initializes a new Names Endpoint."""
        super(Names, self).__init__(plasticity)
        self.url = self.plasticity.sapien.url + "names/"

    def post(self, name, pretty=False):
        """Makes a post to the Names API.

        Runs the name with the requested parameters through the Sapien
        Names API.
        :param name: The name to analyze
        :type name: str
        :param pretty: Whether or not to pretty print, defaults to False
        :type pretty: bool, optional
        :returns: The response from the API endpoint
        :rtype: {NamesResponse}
        """
        payload = json.dumps({
            'name': name,
            'pretty': pretty,
        })
        res = self.plasticity._post(self.url, payload)
        return NamesResponse.from_json(res, pretty_enabled=pretty)


class NamesResponse(Response):
    """Holds the `NamesResponse` data from a Names API call."""
    def __init__(self, *args, **kwargs):
        super(NamesResponse, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<NamesResponse %s>' % id(self)

    def __str__(self):
        return '<NamesResponse %s>' % id(self)

    def is_male_name(self):
        is_male = utils.deep_get(self.data, 'isMaleName', 'value')
        is_certain = utils.deep_get(
            self.data, 'isMaleName', 'confidence') == 'Certain'
        return is_male and is_certain

    def is_female_name(self):
        is_female = utils.deep_get(self.data, 'isFemaleName', 'value')
        is_certain = utils.deep_get(
            self.data, 'isFemaleName', 'confidence') == 'Certain'
        return is_female and is_certain

    def is_first_name(self):
        is_male = utils.deep_get(self.data, 'isMaleName', 'value')
        is_m_certain = utils.deep_get(
            self.data, 'isMaleName', 'confidence') == 'Certain'
        is_female = utils.deep_get(self.data, 'isFemaleName', 'value')
        is_f_certain = utils.deep_get(
            self.data, 'isFemaleName', 'confidence') == 'Certain'
        return (is_male and is_m_certain) or (is_female and is_f_certain)

    def is_family_name(self):
        is_family_name = utils.deep_get(self.data, 'isFamilyName', 'value')
        is_certain = utils.deep_get(
            self.data, 'isFamilyName', 'confidence') == 'Certain'
        return is_family_name and is_certain

    def is_name(self):
        is_name = utils.deep_get(self.data, 'isName', 'value')
        is_certain = utils.deep_get(
            self.data, 'isName', 'confidence') == 'Certain'
        return is_name and is_certain
