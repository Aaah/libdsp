import pytest as pytest

from libdsp.parameters import *

__author__ = "Rémy VINCENT"
__copyright__ = "Aaah"
__license__ = "Copyright 2022"


def test_parameters_template():
    """Check instance"""
    param = DSPModuleParameter(name="name", descp="description")
    assert isinstance(param, DSPModuleParameter)
    return


def test_parameters_float_1():
    """Check instance"""
    param = DSPModuleParameterFloat(
        name="name",
        descp="description",
        units="dB",
        minv=0,
        maxv=1,
        initv=0.0,
        stepv=0.001,
    )
    assert isinstance(param, DSPModuleParameterFloat)
    return


def test_parameters_float_2():
    """Check the repr of the float parameter"""
    param = DSPModuleParameterFloat(
        name="parameter name",
        descp="description of the parameter",
        units="dB",
        minv=0,
        maxv=1,
        initv=0.0,
        stepv=0.001,
    )
    info = repr(param)
    assert len(info)
    return


def test_parameters_float_2():
    """Check the validity of the type in the valid set of values"""
    p1 = DSPModuleParameterFloat(name="parameter name", set=[1.0, 2.0, 3.0])
    assert isinstance(p1, DSPModuleParameterFloat)

    return


def test_parameters_float_3():
    """Check the validity of the type in the valid set of values"""
    with pytest.raises(Exception):
        p1 = DSPModuleParameterFloat(
            name="parameter name", set=["not a float", 2.0, 3.0]
        )

    return


p1 = DSPModuleParameterFloat(name="parameter name", set=[1.0, 2.0, 3.0])

print(repr(p1))
