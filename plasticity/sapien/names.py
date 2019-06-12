from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from plasticity.utils import utils
from plasticity.base.endpoint import Endpoint


class Names(Endpoint):
    """The Names Endpoint performs all the Names API functions
    described here: https://www.plasticity.ai/api/docs/#sapien-names

    Basic usage:

    ```python
    plasticity.sapien.names.post('bill gates')
    ```


    Arguments:

    name: required
    pretty: optional, defaults to False

    ```python
    plasticity.sapien.names.post('mary')
    ```


    Returns:

    This returns a custom `Names.Response`, which has additional helper
    functions from the default `Response` documented in the `Names.Response`
    class below.

    ```python
    result = plasticity.sapien.names.post('sarah')
    print(result.is_female_name)  # True
    ```
    """
    NAME = 'Names'
    PARAMS = [
        ('name',),
        ('pretty', False)
    ]

    def __init__(self, plasticity):
        """Initializes a new Names Endpoint."""
        super(Names, self).__init__(plasticity)
        self.url = self.plasticity.sapien.url + 'names/'

    class Response(Endpoint.Response):
        def is_male_name(self):
            """Checks if a name is male, with certainty.

            :returns: Whether the name is male
            :rtype: {bool}
            """
            is_male = utils.deep_get(self.data, 'isMaleName', 'value')
            is_certain = utils.deep_get(
                self.data, 'isMaleName', 'confidence') == 'Certain'
            return is_male and is_certain

        def is_female_name(self):
            """Checks if a name is female, with certainty.

            :returns: Whether the name is female
            :rtype: {bool}
            """
            is_female = utils.deep_get(self.data, 'isFemaleName', 'value')
            is_certain = utils.deep_get(
                self.data, 'isFemaleName', 'confidence') == 'Certain'
            return is_female and is_certain

        def is_first_name(self):
            """Checks if a name is a first name, with certainty.

            :returns: Whether the name is a first name
            :rtype: {bool}
            """
            is_male = utils.deep_get(self.data, 'isMaleName', 'value')
            is_m_certain = utils.deep_get(
                self.data, 'isMaleName', 'confidence') == 'Certain'
            is_female = utils.deep_get(self.data, 'isFemaleName', 'value')
            is_f_certain = utils.deep_get(
                self.data, 'isFemaleName', 'confidence') == 'Certain'
            return (is_male and is_m_certain) or (is_female and is_f_certain)

        def is_family_name(self):
            """Checks if a name is a family name, with certainty.

            :returns: Whether the name is a family name
            :rtype: {bool}
            """
            is_family_name = utils.deep_get(self.data, 'isFamilyName', 'value')
            is_certain = utils.deep_get(
                self.data, 'isFamilyName', 'confidence') == 'Certain'
            return is_family_name and is_certain

        def is_name(self):
            """Checks if the text supplied is a name, with certainty.

            :returns: Whether the text is a name
            :rtype: {bool}
            """
            is_name = utils.deep_get(self.data, 'isName', 'value')
            is_certain = utils.deep_get(
                self.data, 'isName', 'confidence') == 'Certain'
            return is_name and is_certain
