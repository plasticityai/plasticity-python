from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import requests

from plasticity.utils import utils


class Endpoint(object):
    """An Endpoint is a specific API action within an API service.

    Attributes:
        plasticity: a Plasticity instance with the API URL and token
    """
    def __init__(self, plasticity):
        """Initializes a new Endpoint."""
        self.plasticity = plasticity
        self.headers = {}
        self.headers['content-type'] = 'application/json'
        if self.plasticity.token:
            self.headers['authorization'] = 'Bearer ' + self.plasticity.token

    @classmethod
    def get_param_default(cls, param):
        for p in cls.PARAMS:
            if p[0] == param:
                return p[1]
        return None

    @classmethod
    def get_payload_from_args(cls, args, kwargs):
        if isinstance(args[0], dict):
            data = args[0]
        else:
            data = {}
            for i, param in enumerate(cls.PARAMS):
                args_lookup = (args[i:i+1] or (None,))[0]
                if args_lookup is not None:
                    data[param[0]] = args_lookup
            data.update(kwargs)
        return data

    def _request(self, method, *args, **kwargs):
        payload = self.get_payload_from_args(args, kwargs)
        try:
            response = requests.request(
                method, self.url, data=json.dumps(payload),
                headers=self.headers)
        except requests.exceptions.Timeout:
            raise self.PlasticityAPITimeoutError('The request timed out.')
        return self.Response(response)

    def post(self, *args, **kwargs):
        return self._request('POST', *args, **kwargs)

    def get(self, *args, **kwargs):
        return self._request('GET', *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self._request('DELETE', *args, **kwargs)

    class Response(object):
        """A Response is a specific API response to an API endpoint.

        Attributes:
            plasticity: a Plasticity instance with the API URL and token
        """
        def __init__(self, response):
            self._response = response
            self._request = response.request

            try:
                self.response = json.loads(response.text)
            except ValueError:
                self.response = json.loads(
                    response.text[:response.text.rfind('<!DOCTYPE')])
            self.request = json.loads(self._request.body)

            self.data = self.response.get('data')
            self.error = self.response.get('error', False)
            self.error_code = self.response.get('errorCode', 200)
            self.error_message = self.response.get('message', '')

        def __repr__(self):
            return '<Response {}>'.format(id(self))

        def __str__(self):
            output = 'Response'
            if self.error:
                output += ' - {} error:'.format(self.error_code)
                output += '\n'
                output += utils.indent(
                    utils.shorten('{}'.format(self.error_message)))
            else:
                output = '<Response {}>'.format(self.response)
            return output

    class PlasticityAPITimeoutError(Exception):
        """Raised when the API connection has timed out."""
        pass
