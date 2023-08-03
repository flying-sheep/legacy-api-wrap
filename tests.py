from inspect import signature

import pytest

from legacy_api_wrap import legacy_api


# def old(a, b=None, d=1, c=2):
# 	pass
@legacy_api("d", "c")
def new(a, b=None, *, c=2, d=1, e=3):
    return dict(a=a, b=b, c=c, d=d, e=e)


def test_inspection_correct():
    assert str(signature(new)) == "(a, b=None, *, c=2, d=1, e=3)"


def test_new_param_available():
    new(12, e=13)


def test_old_positional_order():
    with pytest.deprecated_call():
        res = new(12, 13, 14)
    assert res["d"] == 14


def test_warning_stack():
    with pytest.deprecated_call() as record:
        new(12, 13, 14)
    w = record.pop()  # type: warnings.WarningMessage
    assert w.filename == __file__


def test_too_many_args():
    from pytest import raises

    with raises(TypeError, match=r"new\(\) takes from 1 to 4 parameters, but 5 were given\."):
        new(1, 2, 3, 4, 5)
