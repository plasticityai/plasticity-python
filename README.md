# plasticity-python
A Python module for using the [Plasticity API](https://www.plasticity.ai/api/docs).

## Installation
This module is available on PyPi and can be installed with pip, a
package manager for Python. To install, just run:

```sh
pip install plasticity
```

To install from source (for development, etc.), run:

```sh
pip install git+https://github.com/plasticityai/plasticity-python.git
```

## Getting Started
Getting started with the Plasticity API is easy. Simply create a `Plasticity`
object and you can start using it.

### API Tokens
The `Plasticity` object needs your API credentials. You can either pass these
directly to the constructor (see the code below) or via environment variables.

```python
from plasticity import Plasticity
plasticity = Plasticity('<YOUR_TOKEN>')
```

Alternately, a Plasticity constructor without these parameters will look for
the `PLASTICITY_API_KEY` variable inside the current environment. We suggest storing your credentials as environment variables so that you don't
accidentally post them somewhere public.

```python
from plasticity import Plasticity
plasticity = Plasticity()
```

### Making a Call
Generally, the library attempts to mirror the Plasticity API service as closely
as possible. It also makes several helper classes available to quickly analyze
and use the API's responses.

```python
from plasticity import Plasticity

plasticity = Plasticity('<YOUR_TOKEN>')
result = plasticity.sapien.core.post('This is an example of the Plasticity python package.')
print(result)  # A pretty form of the `Response` object
```

Above you'll notice the format for these calls is usually:
`plasticity.<service>.<endpoint>.{post|get}(<params>)`.

Additional documentation for endpoint calls can be found in the corresponding
endpoint file, located in `plasticity/<service>/<endpoint>.py`.

### Accessing the `Response`
These calls will return a `Response` object with the API data, or an error
if one occurred.

```python
from plasticity import Plasticity

plasticity = Plasticity('<YOUR_TOKEN>')
result = plasticity.sapien.core.post('If this works, error will be False.')
print(result.error)  # False, if no error
```

Certain endpoints have custom `Response` objects that also
implement several helper functions to assist in making use of the response data.

```python
from plasticity import Plasticity

plasticity = Plasticity('<YOUR_TOKEN>')
result = plasticity.sapien.core.post('The Response object contains data and helper methods.')
tpls = result.tpls()
print(tpls)  # [[[u'The', u'DT', u'the'], ..., [u'.', u'PERIOD', u'.']]]
```

Additional documentation for endpoint `Response` objects can be found in the
corresponding endpoint file, located in `plasticity/<service>/<endpoint>.py`.

## Help & Contributing
If you need help using the library, please contact us at
[opensource@plasticity.ai](mailto:opensource@plasticity.ai).

The main repository for this project can be found on
[GitLab](https://gitlab.com/Plasticity/plasticity-python). The GitHub
repository is only a mirror. If you've found a bug in the library or would
like new features added, please open issues or pull requests!
