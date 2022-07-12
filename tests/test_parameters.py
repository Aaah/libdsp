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
