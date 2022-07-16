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
        range: list = None,
    ) -> None:
        self._dtype = dtype  # data type allowed, unique for each variable
        self._val = None  # the value of the variable
        self._status = status  # can the value be edited
        self._range = None  # ranged numerical values
        self._set = None  # set of allowed values (numbers, strings)

        # handle numerical range
        if range is not None:

            # raise error if dtype=string
            if self._dtype == str:
                raise ValueError(
                    "DSPVariable RANGE : not compatible with datatype <string>, expect numerical datatype"
                )

            # raise error if set is not None
            if self._set is not None:
                raise ValueError(
                    "DSPVariable RANGE : conflict with SET also defined, but cannot be used at the same time"
                )

            self._range = {}

            # check datatype in the range list
            for e in range:
                if not isinstance(e, self._dtype):
                    raise ValueError(
                        "DSPVariable RANGE : mismatch of types, expected %s but got %s."
                        % (self._dtype, type(e))
                    )

            # store elements
            if len(range) < 3 or len(range) > 4:
                raise ValueError(
                    "DSPVariable RANGE : expected 3 or 4 parameters to describe the range (min, step, max, (default)) but got %d"
                    % len(status)
                )

            if len(range) >= 3:
                self._range["minv"] = range[0]
                self._range["stepv"] = range[1]
                self._range["maxv"] = range[2]
                self._range["default"] = self._range["minv"]

            if len(range) == 4:
                self._range["default"] = range[3]

            # raise exception if minv > maxv
            if self._range["minv"] > self._range["maxv"]:
                raise ValueError(
                    "DSPVariable RANGE : minv (%s) > maxv (%s)"
                    % (str(self._range["minv"], self._range["maxv"]))
                )

            # initialise value
            self.val = self._range["default"]

        pass

    def __repr__(self) -> str:
        # todo range/set...
        return "(%s, %s, %s)" % (str(self._val), str(self._dtype), str(self._status))

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, v):

        # handle datatype mismatch
        if not isinstance(v, self._dtype):
            raise ValueError(
                "DSPVariable value SETTER : the candidate variable has improper type, expected %s but got %s."
                % (self._dtype, type(v))
            )

        # enable setter for dynamic variables only
        if self._status == DSPVariableStatus.DSP_VAR_DYNAMIC:

            # handle numerical ranged variables
            if self._range is not None:

                # round with given accuracy
                self._val = np.round(v / self._range["stepv"]) * self._range["stepv"]

                # apply boundaries to the candidate value
                self._val = np.clip(self._val, self._range["minv"], self._range["maxv"])

                # make sure to preserv data type (above operations switch to float64)
                self._val = self._dtype(self._val)

                return

            # by default, accept value
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
