from __future__ import annotations

from inspect import signature

import pytest

from legacy_api_wrap import legacy_api


# def old(a, b=None, d=1, c=2):
# 	pass
@legacy_api("d", "c")
def new(a, b=None, *, c=2, d=1, e=3):  # type: ignore[no-untyped-def] # noqa: ANN001, ANN201
    return {"a": a, "b": b, "c": c, "d": d, "e": e}


def test_inspection_correct() -> None:
    assert str(signature(new)) == "(a, b=None, *, c=2, d=1, e=3)"


def test_new_param_available() -> None:
    new(12, e=13)


def test_old_positional_order() -> None:
    with pytest.deprecated_call():
        res = new(12, 13, 14)  # type: ignore[misc]
    assert res["d"] == 14


def test_warning_stack() -> None:
    with pytest.deprecated_call() as record:
        new(12, 13, 14)  # type: ignore[misc]
    w = record.pop()
    assert w.filename == __file__


def test_too_many_args() -> None:
    with pytest.raises(
        TypeError,
        match=r"new\(\) takes from 1 to 4 parameters, but 5 were given\.",
    ):
        new(1, 2, 3, 4, 5)  # type: ignore[misc]


def test_customize() -> None:
    @legacy_api("a", category=FutureWarning)
    def new(*, a: int) -> int:
        return a

    with pytest.raises(FutureWarning):
        new(1)
