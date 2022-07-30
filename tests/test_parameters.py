import mock
import pytest as pytest

from libdsp.parameters import *
from libdsp.tools import *

__author__ = "Rémy VINCENT"
__copyright__ = "Aaah"
__license__ = "Copyright 2022"


"""

- [x] instance

- [x] set/get the status (lock/unlock)
- [x] number/range : get/set the value (int, bool, float)
- [ ] number/set : get/set the value (int, bool, float)
- [ ] str/format : get/set the value
- [ ] str/set : get/set the value

- [x] callback : check call
- [x] callback : only if value is different
- [ ] push/pull callbacks
- [ ] several callbacks

- [ ] link parameters : change value
- [ ] link parameters : lock value from direct setter
- [ ] link parameters : check callback calls



"""


def test_parameters_1():
    """instance"""
    param = DSPParameter(name="param1", var=DSPVariable(float))
    assert isinstance(param, DSPParameter)

    return


def test_parameters_number_range_1():
    """get/set the value (int, float)"""

    param = DSPParameter(name="param1", var=DSPVariable(float, range=(0.0, 0.1, 1.0)))
    param.val = 0.3
    assert almost_equal(param.val, 0.3)

    pass


def test_parameters_number_range_2():
    """get/set the value (int, float)"""

    param = DSPParameter(name="param1", var=DSPVariable(int, range=(0, 1, 100)))
    param.val = 33
    assert param.val == 33

    pass


def test_parameters_number_boolean():
    """get/set the value"""

    param = DSPParameter(name="param1", var=DSPVariable(bool))
    param.val = False
    assert param.val == False

    param.val = True
    assert param.val == True

    pass


def test_parameters_status():
    """lock/unlock the update of the parameter value"""
    param = DSPParameter(name="param1", var=DSPVariable(bool))

    param.lock()
    assert param.status == DSPVariableStatus.DSP_VAR_CONSTANT

    param.unlock()
    assert param.status == DSPVariableStatus.DSP_VAR_DYNAMIC

    pass


def test_parameters_callback_1():
    """check call"""

    param = DSPParameter(name="param1", var=DSPVariable(bool))
    cb = mock.Mock()  # create mock callback
    param.push_callback(cb)  # ... and attach it
    assert cb.call_count == 0

    # callback on value change
    param.val = True
    assert cb.call_count == 1

    # not on identical value
    param.val = True
    assert cb.call_count == 1

    pass


def test_parameters_link_1():
    """basic valid linkage"""

    p1 = DSPParameter(name="p1", var=DSPVariable(float, range=(0.0, 0.1, 1.0)))
    p2 = DSPParameter(name="p2", var=DSPVariable(float, range=(0.0, 0.1, 1.0)))

    # compatible link
    assert p1.link(p2) == 0

    # valid value change
    p1.val = 0.3
    assert almost_equal(p1.val == 0.3)
    assert almost_equal(p2.val == 0.3)

    # mirror
    p2.val = 0.5
    assert almost_equal(p1.val == 0.5)
    assert almost_equal(p2.val == 0.5)

    # unlink
    p1.unlink(p2)
    p1.val = 0.6
    assert almost_equal(p1.val == 0.6)
    assert almost_equal(p2.val == 0.3)

    pass


def test_parameters_link_2():
    """basic invalid linkage"""

    p1 = DSPParameter(name="p1", var=DSPVariable(float, range=(0.0, 0.1, 1.0)))
    p2 = 3.0  # not a parameter

    # uncompatible link
    with pytest.raises(Exception):
        p1.link(p2)

    pass


def test_parameters_link_3():
    """valid not obvious linkage"""

    p1 = DSPParameter(name="p1", var=DSPVariable(float, range=(0.0, 0.1, 1.0)))
    p2 = DSPParameter(name="p2", var=DSPVariable(float, set=(0.0, 0.5, 1.0)))

    # valid link
    assert p1.link(p2) == 0

    # valid negotiation
    p1.val = 0.5
    assert almost_equal(p1.val == 0.5)
    assert almost_equal(p2.val == 0.5)

    # invalid negotiation
    p1.val = 0.3
    assert almost_equal(p1.val == 0.5)
    assert almost_equal(p2.val == 0.5)

    pass


def test_parameters_link_4():
    """invalid linkage because of dtype"""

    p1 = DSPParameter(name="p1", var=DSPVariable(int, range=(0, 1, 10)))
    p2 = DSPParameter(name="p2", var=DSPVariable(float, range=(0.0, 0.5, 1.0)))

    # uncompatible link
    assert p1.link(p2) == -1

    pass


def test_parameters_link_5():
    """linkage set - set"""

    p1 = DSPParameter(name="p1", var=DSPVariable(int, set=(0, 1, 2)))
    p2 = DSPParameter(name="p2", var=DSPVariable(int, set=(1, 2, 5)))

    # valid link
    assert p1.link(p2) == 0

    # the resulting active set is identical
    assert p1._var._set == p2._var._set

    # the expected set
    assert p1._var._set == [1, 2]

    # the default value is the first in the resulting set
    assert p1.val == 1
    assert p2.val == 1

    pass
