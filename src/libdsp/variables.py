import numpy as np

__author__ = "Rémy VINCENT"
__copyright__ = "Aaah"
__license__ = "Copyright 2022"

"""

VARIABLES are used as containers for any atomic information, either numeric of alpha.

Usages :
- setup algorithms via "module parameters"
- handle connections between sink/source signals via negotiations (range of capabilities, fixed or not)

A variable can lie within a range or a set.

Numerical values :
- range : bounds and default value
- set : list of available values

String :
- range : format
- set : list of available values (much like an enum)

"""


class DSPVariable:
    def __init__(self, dtype: np.dtype) -> None:
        self._dtype = dtype  # data type allowed, unique for each variable
        self._val = None  # the value of the variable
        pass

    def __repr__(self) -> str:
        return "(%s, %s)" % (self._val, self._dtype)

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, v):
        if not isinstance(v, self._dtype):
            raise ValueError(
                "DSPVariable SETTER : the candidate variable has improper type, expected %s but got %s."
                % (self._dtype, type(v))
            )
        self._val = v
        pass
