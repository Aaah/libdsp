from enum import Enum

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


class DSPVariableStatus(Enum):
    DSP_VAR_CONSTANT = 0  # the value cannot be changed
    DSP_VAR_DYNAMIC = 1  # the value can be changed using the setter


class DSPVariable:
    def __init__(
        self,
        dtype: np.dtype,
        status: DSPVariableStatus = DSPVariableStatus.DSP_VAR_DYNAMIC,
    ) -> None:
        self._dtype = dtype  # data type allowed, unique for each variable
        self._val = None  # the value of the variable
        self._status = status  # can the value be edited
        pass

    def __repr__(self) -> str:
        return "(%s, %s, %s)" % (str(self._val), str(self._dtype), str(self._status))

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

        if self._status == DSPVariableStatus.DSP_VAR_DYNAMIC:
            self._val = v

        return

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, s: DSPVariableStatus):
        self._status = s
        pass


# class DSPNumber(DSPVariable):
