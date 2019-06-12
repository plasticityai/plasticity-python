from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from plasticity.base.endpoint import Endpoint


class Transform(Endpoint):
    """The Transform Endpoint performs all the Transform API functions
    described here: https://www.plasticity.ai/api/docs/#sapien-transform

    Basic usage:

    ```python
    plasticity.sapien.transform.post('leaf', 'NounPlural')
    ```


    Arguments:

    word: required
    action: required (any of the values suggested here:
            https://www.plasticity.ai/api/docs/#sapien-transform)
    pretty: optional, defaults to False

    ```python
    plasticity.sapien.transform.post('eating', 'VerbPast')
    ```


    Returns:

    This returns a default `Response`. You can access the result of the
    transformation using the `data` property.

    ```python
    result = plasticity.sapien.transform.post('eating', 'VerbPast')
    print(result.data)  # ate
    ```
    """
    NAME = 'Transform'
    PARAMS = [
        ('word',),
        ('action',),
        ('pretty', False)
    ]

    def __init__(self, plasticity):
        """Initializes a new Transform Endpoint."""
        super(Transform, self).__init__(plasticity)
        self.url = self.plasticity.sapien.url + 'transform/'
