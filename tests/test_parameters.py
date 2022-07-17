import pytest as pytest

from libdsp.parameters import *

__author__ = "Rémy VINCENT"
__copyright__ = "Aaah"
__license__ = "Copyright 2022"


"""

- [+] instance

- [ ] set/get the status
- [+] number/range : get/set the value (int, bool, float)
- [ ] number/set : get/set the value (int, bool, float)
- [ ] str/format : get/set the value
- [ ] str/set : get/set the value

- [ ] callback : check call
- [ ] callback : only if value is different


"""


def almost_equal(x, y, tol=0.0000001):
    return True if np.abs(x - y) < tol else False


def test_parameters_1():
    """instance"""
    param = DSPModuleParameter(name="param1", var=DSPVariable(float))
    assert isinstance(param, DSPModuleParameter)

    return


def test_parameters_number_range_1():
    """get/set the value (int, float)"""

    param = DSPModuleParameter(
        name="param1", var=DSPVariable(float, range=(0.0, 0.1, 1.0))
    )
    param.val = 0.3
    assert almost_equal(param.val, 0.3)

    pass


def test_parameters_number_range_2():
    """get/set the value (int, float)"""

    param = DSPModuleParameter(name="param1", var=DSPVariable(int, range=(0, 1, 100)))
    param.val = 33
    assert param.val == 33

    pass


def test_parameters_number_boolean():
    """get/set the value"""

    param = DSPModuleParameter(name="param1", var=DSPVariable(bool))
    param.val = False
    assert param.val == False

    param.val = True
    assert param.val == True

    pass
