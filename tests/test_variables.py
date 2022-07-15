import pytest as pytest

from libdsp.variables import *

__author__ = "Rémy VINCENT"
__copyright__ = "Aaah"
__license__ = "Copyright 2022"

"""
- [x] any: check datatype for floats/int/booleans/string
- [ ] any/negotiation: try change a fixed value
- [ ] any/negotiation: change status to constrained/negotiable
- [ ] any: repr

- [ ] number/range: bounds
- [ ] number/set: in/out of set

- [ ] string/format: in/out format
- [ ] string/set: in/out set
"""


def almost_equal(x, y, tol=0.0000001):
    return True if np.abs(x - y) < tol else False


def test_variable_1():
    """datatype float"""

    var = DSPVariable(dtype=float)  # correspond to np.float64

    # basic set
    rdm_float = np.random.uniform(0.0, 1.0)
    var.val = rdm_float
    assert almost_equal(var.val, rdm_float)

    # type conflict
    with pytest.raises(Exception):
        var.val = "not a float"

    pass


def test_variable_2():
    """datatype int"""

    var = DSPVariable(dtype=np.int16)

    # basic set
    rdm_int = np.random.randint(0, 3458, dtype=np.int16)
    var.val = rdm_int
    assert var.val == rdm_int

    # type conflict
    rdm_int = np.random.randint(0, 3458, dtype=np.int32)
    with pytest.raises(Exception):
        var.val = rdm_int

    pass


def test_variable_3():
    """datatype boolean"""

    var = DSPVariable(dtype=np.bool8)

    # basic set
    rdm_bool = np.random.choice([True, False])
    var.val = rdm_bool
    assert var.val == rdm_bool

    # type conflict
    rdm_int = np.random.randint(0, 3458, dtype=np.int32)
    with pytest.raises(Exception):
        var.val = rdm_int

    pass


def test_variable_4():
    """datatype string"""

    var = DSPVariable(dtype=str)

    # basic set
    rdm_str = "this is not a random string"
    var.val = rdm_str
    assert var.val == rdm_str

    # type conflict
    rdm_int = np.random.randint(0, 3458, 1, dtype=np.int32)
    with pytest.raises(Exception):
        var.val = rdm_int

    pass


def test_variable_5():
    """status"""

    # default status
    var = DSPVariable(dtype=float, status=DSPVariableStatus.DSP_VAR_DYNAMIC)
    assert var.status == DSPVariableStatus.DSP_VAR_DYNAMIC

    # change status
    var.status = DSPVariableStatus.DSP_VAR_CONSTANT
    assert var.status == DSPVariableStatus.DSP_VAR_CONSTANT

    # try and change value when constant
    ref_value = var.val
    var.val = 1.0
    assert var.val is ref_value

    pass
