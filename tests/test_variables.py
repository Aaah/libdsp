import pytest as pytest

from libdsp.variables import *

__author__ = "Rémy VINCENT"
__copyright__ = "Aaah"
__license__ = "Copyright 2022"

"""
- [x] any: check datatype for floats/int/booleans/string
- [x] any/negotiation: try change a fixed value
- [x] any/negotiation: change status to constrained/negotiable
- [ ] any: repr

- [x] number/range: mistake on range (dtype)
- [x] number/range: special cases on bounds (min > max, step > max-min)
- [x] number/range: bounds (float/int)
- [x] number/range: roundings based on step value (float)
- [x] number/set-range: conflict if the 2 are defined
- [x] number/string: conflict if string + range
- [x] number/range: check preservation of format after roundings (int, floats)

- [x] number/set: in/out of set

- [ ] bool : set with range and check that it is ignored

- [ ] string/format: in/out format
- [ ] string/set: in/out set
"""


def almost_equal(x, y, tol=0.0000001):
    return True if np.abs(x - y) < tol else False


def test_variable_1():
    """datatype float"""

    with pytest.raises(Exception):
        var = DSPVariable(dtype=float)

    var = DSPVariable(
        dtype=float, range=[0.0, 0.0000000001, 1.0]
    )  # correspond to np.float64

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

    with pytest.raises(Exception):
        var = DSPVariable(dtype=np.int16)

    var = DSPVariable(dtype=int, range=[0, 1, 3458])

    # basic set
    rdm_int = np.random.randint(0, 3458, dtype=int)
    var.val = rdm_int
    assert var.val == rdm_int

    # type conflict
    rdm_int = np.random.randint(0, 3458, dtype=np.int16)
    with pytest.raises(Exception):
        var.val = rdm_int

    pass


def test_variable_3():
    """datatype boolean"""

    var = DSPVariable(dtype=bool)

    # basic set
    rdm_bool = True
    var.val = rdm_bool
    assert var.val == rdm_bool

    rdm_bool = False
    var.val = rdm_bool
    assert var.val == rdm_bool

    # type conflict
    rdm_int = np.random.randint(0, 3458, dtype=np.int32)
    with pytest.raises(Exception):
        var.val = rdm_int

    pass


# def test_variable_4():
#     """datatype string"""

#     var = DSPVariable(dtype=str, set=["un", "deux", "trois"])

#     # basic set
#     rdm_str = "this is not a random string"
#     var.val = rdm_str
#     assert var.val == rdm_str

#     # type conflict
#     rdm_int = np.random.randint(0, 3458, 1, dtype=np.int32)
#     with pytest.raises(Exception):
#         var.val = rdm_int

#     pass


def test_variable_5():
    """status"""

    # default status
    var = DSPVariable(
        dtype=float, status=DSPVariableStatus.DSP_VAR_DYNAMIC, set=[0.0, 1.0]
    )
    assert var.status == DSPVariableStatus.DSP_VAR_DYNAMIC

    # change status
    var.status = DSPVariableStatus.DSP_VAR_CONSTANT
    assert var.status == DSPVariableStatus.DSP_VAR_CONSTANT

    # try and change value when constant
    ref_value = var.val
    var.val = 1.0
    assert var.val is ref_value

    pass


def test_variable_number_range_1():
    """roundings"""

    # create a float within a range
    var = DSPVariable(dtype=float, range=[0.0, 0.1, 1.0, 0.0])

    # acceptable set
    var.val = 0.5
    assert almost_equal(var.val, 0.5)

    # roundings with given accuracy
    var.val = 0.54
    assert almost_equal(var.val, 0.5)

    var.val = 0.55
    assert almost_equal(var.val, 0.6)

    var.val = 0.56
    assert almost_equal(var.val, 0.6)

    pass


def test_variable_number_range_2():
    """bounds for floats"""

    minv = 0.0
    stepv = 0.1
    maxv = 1.0

    # create a float within a range
    var = DSPVariable(dtype=float, range=[minv, stepv, maxv, 0.0])

    # undershoot
    var.val = -1.0
    assert almost_equal(var.val, minv)

    # overshoot
    var.val = 1.2
    assert almost_equal(var.val, maxv)

    pass


def test_variable_number_range_3():
    """bounds for int"""

    minv = 0
    stepv = 2
    maxv = 100

    # create a float within a range
    var = DSPVariable(dtype=int, range=[minv, stepv, maxv, 0])

    # undershoot
    var.val = minv - 10
    assert almost_equal(var.val, minv)

    # overshoot
    var.val = maxv + 10
    assert almost_equal(var.val, maxv)

    pass


def test_variable_number_range_4():
    """mistake on range dtype"""

    minv = 0.0  # a float, not int
    stepv = 1
    maxv = 100

    # create a variable
    with pytest.raises(Exception):
        var = DSPVariable(dtype=np.int16, range=[minv, stepv, maxv, 0])

    pass


def test_variable_number_range_5():
    """special cases on boundaries"""

    # default value is out of bounds
    var = DSPVariable(dtype=float, range=[0.0, 0.1, 1.0, 2.0])
    assert almost_equal(var.val, 1.0)

    # minv > maxv
    with pytest.raises(Exception):
        var = DSPVariable(dtype=float, range=[1.0, 0.1, 0.0])

    # step > maxv-minv
    var = DSPVariable(dtype=float, range=[0.0, 1.1, 1.0])
    assert almost_equal(var.val, 0.0)
    var.val = 0.6
    assert almost_equal(var.val, 1.0)

    pass


def test_variable_number_range_6():
    """roundings, check preservation of datatype"""

    # check for floats
    var = DSPVariable(dtype=float, range=[0.0, 0.1, 1.0, 0.0])
    var.val = 0.53
    assert almost_equal(var.val, 0.5)
    assert isinstance(var.val, float)

    # check for ints
    var = DSPVariable(dtype=int, range=[0, 3, 100, 3])
    assert var.val == 3
    assert isinstance(var.val, int)

    var.val = 37
    assert var.val == 36
    assert isinstance(var.val, int)

    return


def test_variable_number_range_set_conflict():
    """conflict if both set and range are defined"""

    with pytest.raises(Exception):
        var = DSPVariable(dtype=float, range=[0.0, 0.1, 1.0, 2.0], set=[0.0, 1.0])

    pass


def test_variable_number_range_string_conflict():
    """conflict if a range is called on a string variable"""

    with pytest.raises(Exception):
        var = DSPVariable(dtype=str, range=[0.0, 0.1, 1.0, 2.0])

    pass


def test_variable_number_set_1():
    """empty set on definition"""

    with pytest.raises(Exception):
        var = DSPVariable(dtype=int, set=[])

    pass


def test_variable_number_set_2():
    """invalid datatype in a set definition"""

    with pytest.raises(Exception):
        var = DSPVariable(dtype=int, set=[0, 1.0, 3])

    pass


def test_variable_number_set_3():
    """basic valid set definition"""

    var = DSPVariable(dtype=int, set=[0, 1, 2, 3])

    # check the resulting set
    assert var._set == [0, 1, 2, 3]

    # check the capabilities are defined
    assert var._set_caps == var._set

    pass


def test_variable_number_set_4():
    """set trials for ints"""

    var = DSPVariable(dtype=int, set=[0, 1, 2, 3])

    # valid value
    var.val = 2
    assert var.val == 2

    # invalid value
    var.val = -1
    assert var.val == 2

    # invalid dtype
    with pytest.raises(Exception):
        var.val = "not an int"

    pass


def test_variable_number_set_5():
    """set trials for floats"""

    var = DSPVariable(dtype=float, set=[0.0, 1.0, 2.0, 3.0])

    # valid value
    var.val = 2.0
    assert var.val == 2.0

    # invalid value
    var.val = -1.0
    assert var.val == 2.0

    # invalid dtype
    with pytest.raises(Exception):
        var.val = "not an int"

    pass
