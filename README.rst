unleashed-py
============

.. image:: https://img.shields.io/pypi/v/unleashed-py.svg
    :target: https://pypi.python.org/pypi/unleashed-py
    :alt: Latest PyPI version

.. image:: https://travis-ci.org/borntyping/cookiecutter-pypackage-minimal.png
   :target: https://travis-ci.org/borntyping/cookiecutter-pypackage-minimal
   :alt: Latest Travis CI build status

Python package to connect to the Unleashed Software inventory management API

Usage
-----
Instantiate a Resource object

resource = Resource(resource_name, auth_id, auth_sig,  api_add, \*\*kwargs)

resource_name will be whichever of the unleashed features you want to extract from the API: Attribute Sets, Bill Of Materials, etc.

where your auth_id, and auth_signature are handed out by Unleashed Software

The api_add is the address to connect to the Unleashed API. Typically https://api.unleashedsoftware.com, but that is subject to change

The keyword arguments are any of the filters that are available for each particular resource.

For full details about potential resources, and available keyword filter arguments see the unleashed api documentation:

https://apidocs.unleashedsoftware.com/

The EditableResource class has a single function for posting information back to the API.

I recommend examining the API docs fully before attempting to upload an object.



Installation
------------
pip install unleashed-py

Requirements
^^^^^^^^^^^^
requests, hmac, hashlib, base64, json, re, & datetime

Compatibility
-------------
Built on python 3.7.3

Licence
-------
MIT

Authors
-------

`unleashed-py` was written by `Jonathan Mucha <jonmucha@gmail.com>`_.
