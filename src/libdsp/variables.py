from enum import Enum

import numpy as np

from libdsp.tools import *

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

# todo : add an optional unit field


class DSPVariableStatus(Enum):
    DSP_VAR_CONSTANT = 0  # the value cannot be changed
    DSP_VAR_DYNAMIC = 1  # the value can be changed using the setter
    DSP_VAR_LINKED = 2  # the value is set by another parameter


class DSPVariable:
    def __init__(
        self,
        dtype: np.dtype,
        status: DSPVariableStatus = DSPVariableStatus.DSP_VAR_DYNAMIC,
        range: list = None,
        set: list = None,
    ) -> None:
        self._dtype = dtype  # data type allowed, unique for each variable
        self._val = None  # the value of the variable
        self._status = status  # can the value be edited

        self._range_caps = None  # initial range (to handle negotiations)
        self._set_caps = None  # initial set (to handle negotiations)
        self._range = None  # active ranged numerical values
        self._set = None  # active set of allowed values (numbers, strings)

        # handle booleans as special case
        if self._dtype == bool:
            self._val = False
            return

        # handle a range type variable
        if isinstance(range, list):

            # raise error if dtype=string
            if self._dtype == str:
                raise ValueError(
                    "DSPVariable RANGE : not compatible with datatype <string>, expect numerical datatype"
                )

            # raise error if set is not None
            if set is not None:
                raise ValueError(
                    "DSPVariable RANGE : conflict with SET also defined, but cannot be used at the same time"
                )

            self._range = {}

            # check datatype in the range list
            # ! to test
            for e in range:
                if not isinstance(e, self._dtype):
                    raise ValueError(
                        "DSPVariable RANGE : mismatch of types, expected %s but got %s."
                        % (self._dtype, type(e))
                    )

            # store elements
            # ! to test
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
            # ! to test
            if self._range["minv"] > self._range["maxv"]:
                raise ValueError(
                    "DSPVariable RANGE : minv (%s) > maxv (%s)"
                    % (str(self._range["minv"], self._range["maxv"]))
                )

            # copy this range as the initial capabilities of the parameter
            self._range_caps = self._range.copy()

            # initialise value
            self.val = self._range["default"]

            return

        # handle a SET type variable
        if isinstance(set, list):

            # raise error if range is not None
            if range is not None:
                raise ValueError(
                    "DSPVariable SET : conflict with RANGE also defined, but cannot be used at the same time"
                )

            # raise error if the set is empty
            if len(set) == 0:
                raise ValueError("DSPVariable SET : set is empty")

            self._set = []

            # check datatype
            for e in set:
                if not isinstance(e, self._dtype):
                    raise ValueError(
                        "DSPVariable SET : mismatch of types, expected %s but got %s."
                        % (self._dtype, type(e))
                    )

            # append values
            for e in set:
                self._set.append(e)

            # copy this set as the initial capabilities of the parameter
            self._set_caps = self._set.copy()

            # initial value (the first one)
            self.val = self._set[0]

            return

        raise ValueError("DSPVariable : no set/range defined")
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

            # handle ranged-type variables
            if self._range is not None:

                # round with given accuracy
                self._val = np.round(v / self._range["stepv"]) * self._range["stepv"]

                # apply boundaries to the candidate value
                self._val = np.clip(self._val, self._range["minv"], self._range["maxv"])

                # make sure to preserv data type (above operations switch to float64)
                self._val = self._dtype(self._val)

                return

            # handle set-type variables
            if self._set is not None:

                # fork strings/numbers
                if self._dtype == str:
                    # ! to test
                    if v in self._set:
                        self._val = v
                        return

                else:

                    for e in self._set:
                        if almost_equal(e, v):
                            self._val = e
                            return

                return

            # default (booleans), accept value
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
