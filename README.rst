Legacy API Wrapper
==================

This module defines a decorator to wrap legacy APIs.
The primary use case is APIs defined before keyword-only parameters.

>>> from legacy_api_wrap import legacy_api

We have a function with many positional parameters lying around:

>>> def fn(a, b=None, d=1, c=2):
...     return c, d, e

We want to convert the positional parameters ``d`` and ``c`` to keyword-only,
change their order and add a parameter. For this we only need to specify name
and order of the old positional parameters in the decorator.

>>> @legacy_api('d', 'c')
... def fn(a, b=None, *, c=2, d=1, e=3):
...     return c, d, e

After adding the decorator, users can keep calling the old API and get a
``DeprecationWarning``:

>>> fn(12, 13, 14) == (2, 14, 3)
True
