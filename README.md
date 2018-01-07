# plasticity-python
A Python module for using the Plasticity API.

## Installation
This module is not yet on pip, a package manager for python. In the meantime,
you can download the source code for `plasticity-python` and setup the module
by running:
```
git clone https://gitlab.com/Plasticity/plasticity-python.git
cd plasticity-python
python setup.py install
```
## Getting Started
Getting started with the Plasticity API is easy. Simply create a `Plasticity` 
object and you can start using it. 

### API Tokens
The `Plasticity` object needs your API credentials. You can either pass these 
directly to the constructor (see the code below) or via environment variables.

```
from plasticity import Plasticity
plasticity = Plasticity("<YOUR_TOKEN>")
```

Alternately, a Plasticity constructor without these parameters will look for 
the PLASTICITY_API_KEY variable inside the current environment.

We suggest storing your credentials as environment variables so that you don't 
accidentally post them somewhere public.

```
from plasticity import Plasticity
plasticity = Plasticity()
```