import pytest as pytest

from libdsp.parameters import *

__author__ = "Rémy VINCENT"
__copyright__ = "Aaah"
__license__ = "Copyright 2022"


def almost_equal(x, y, tol=0.0000001):
    return True if np.abs(x - y) < tol else False


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


def test_parameters_float_4():
    """Check value update in a set"""

    p1 = DSPModuleParameterFloat(name="p1", set=[1.0, 2.0, 3.0])

    # accepted update
    p1.val = 2.0
    assert p1.val == 2.0

    # denied update
    p1.val = -1.0
    assert p1.val == 2.0

    # issue raised because of data type
    with pytest.raises(Exception):
        p1.val = "not a float"

    return


def test_parameters_float_5():
    """Check value update in a range"""
    p1 = DSPModuleParameterFloat(name="p1", minv=0, maxv=1, stepv=0.1)

    # lower bound
    p1.val = -1.0
    assert p1.val == 0.0

    # upper bound
    p1.val = 2.0
    assert p1.val == 1.0

    # standard accepted value
    p1.val = 0.5
    assert almost_equal(p1.val, 0.5)

    # roundings with given accuracy
    p1.val = 0.54
    assert almost_equal(p1.val, 0.5)

    p1.val = 0.55
    assert almost_equal(p1.val, 0.6)

    p1.val = 0.56
    assert almost_equal(p1.val, 0.6)

    return
