"""Legacy API wrapper.

>>> from legacy_api_wrap import legacy_api
>>> @legacy_api('d', 'c')
... def fn(a, b=None, *, c=2, d=1, e=3):
...     return c, d, e
>>> fn(12, 13, 14) == (2, 14, 3)
True
"""

from __future__ import annotations

from functools import wraps
from inspect import Parameter, signature
from typing import TYPE_CHECKING, Callable, TypeVar
from warnings import warn

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import ParamSpec

    P = ParamSpec("P")
    R = TypeVar("R")

INF = float("inf")
POS_TYPES = {Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD}


def legacy_api(*old_positionals: Sequence[str]) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Legacy API wrapper.

    You want to change the API of a function:

    >>> def fn(a, b=None, d=1, c=2, e=3):
    ...     return c, d, e

    Add a the decorator and modify the parameters after the ``*``:

    >>> @legacy_api('d', 'c')
    ... def fn(a, b=None, *, c=2, d=1, e=3):
    ...     return c, d, e

    And the function can be called using one of both signatures.

    >>> fn(12, 13, 14) == (2, 14, 3)
    True

    Parameters
    ----------
    old_positionals
        The positional parameter names that the old function had after the new function’s ``*``.
    """

    def wrapper(fn: Callable[P, R]) -> Callable[P, R]:
        sig = signature(fn)
        par_types = [p.kind for p in sig.parameters.values()]
        has_var = Parameter.VAR_POSITIONAL in par_types
        n_required = sum(1 for p in sig.parameters.values() if p.default is Parameter.empty)
        n_positional = INF if has_var else sum(1 for p in par_types if p in POS_TYPES)

        @wraps(fn)
        def fn_compatible(*args: P.args, **kw: P.kwargs) -> R:
            if len(args) > n_positional:
                args, args_rest = args[:n_positional], args[n_positional:]
                if args_rest:
                    if len(args_rest) > len(old_positionals):
                        n_max = n_positional + len(old_positionals)
                        msg = (
                            f"{fn.__name__}() takes from {n_required} to {n_max} parameters, "
                            f"but {len(args) + len(args_rest)} were given."
                        )
                        raise TypeError(msg)
                    warn(
                        f"The specified parameters {old_positionals[:len(args_rest)]!r} are "
                        "no longer positional. "
                        f"Please specify them like `{old_positionals[0]}={args_rest[0]!r}`",
                        DeprecationWarning,
                        stacklevel=2,
                    )
                    kw = {**kw, **dict(zip(old_positionals, args_rest))}

            return fn(*args, **kw)

        return fn_compatible

    return wrapper
