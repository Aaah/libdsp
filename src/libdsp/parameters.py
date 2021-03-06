import numpy as np

from libdsp.variables import *

__author__ = "Rémy VINCENT"
__copyright__ = "Aaah"
__license__ = "Copyright 2022"

# --- data frames transported from plugins to plugins (inputs, outputs)
# ? can it be achieved with only outputs to avoid memory doubles?

# class PluginIO:
#     def __init__(self, name : str = ""):
#         self._name = name # name of the variable
#         self._data = None # allocated memory to store data
#         self._dims = [] # dimensions of the data
#         self._dtype = None # datatype
#         return

#     @property
#     def data(self):
#         return self._data

#     @data.setter
#     def data(self, v):

#         # memorize the value if the type matches
#         self._data = v

#         # ? alternative : let the connector check once and for all the compatibility of the types?
#         # ? alternative : cast anytime
#         # ? alternative : check datatype and set value if types matches

#         # ? check the dimensions

#         # ? inform that new data has been loaded?

#         pass

# class PluginIOFloat(PluginIO):
#     def __init__(self, name: str = ""):
#         super().__init__(name)

#         # set the type to a float
#         self._dtype = type(0.0)

#         # set the value
#         self.data = float(0.0)

#         return


# --- plugin parameters


class DSPModuleParameter:
    """
    Template class for parameters used to configure DSPModules :
    - they should represent physical quantities as much as possible for clearer use;
    - their attributes are exhaustive enough for automated GUI generation.
    """

    def __init__(self, name: str, var: DSPVariable, descp: str = ""):
        """Initialisation of a DSPModuleParameter.

        Args:
            name (str): name of the parameter.
            var (DSPVariable): variable definition.
            descp (str, optional): quick description of the parameter for hints. Defaults to "".
        """
        self._name = name  # name of the paramter
        self._description = descp  # short description
        self._callbacks = []  # callbacks run when parameter is updated
        self._var = var  # variable instance

        return

    def __repr__(self) -> str:
        """Detailed information about the DSPModuleParameter.

        Returns:
            str: formatted information
        """
        return "%s : %s" % (self._name, self._description)

    @property
    def status(self):
        return self._var.status

    def lock(self):
        self._var.status = DSPVariableStatus.DSP_VAR_CONSTANT
        return

    def unlock(self):
        self._var.status = DSPVariableStatus.DSP_VAR_DYNAMIC
        return

    @property
    def val(self):
        return self._var.val

    @val.setter
    def val(self, v):
        """Setter for the value of the parameter :
        - check for acceptable value (bounds, type...)
        - trigger attached callbacks (typically the configure() method of the DSPModule it is attached to)

        Args:
            v (_type_): candidate value
        """

        # memorize the current value
        ref_v = self._var.val

        # set the value
        self._var.val = v

        # callbacks on value change
        if ref_v != self.val:
            for cb in self._callbacks:
                cb()
        pass


# class DSPModuleParameterFloat(DSPModuleParameter):
#     """
#     A float parameter for DSPModule.
#     """

#     def __init__(
#         self,
#         name: str = "",
#         descp: str = "",
#         set: list = [],
#         units: str = "N/A",
#         minv: float = 0.0,
#         maxv: float = 1.0,
#         initv: float = 0.0,
#         stepv: float = 0.001,
#     ):
#         """Initialisation of a float parameter for DSPModules.

#         If the "set" list is not empty, other parameters are dismissed (minv, maxv, stepv) so that the parameter only tolerates the values included in the set.

#         Args:
#             name (str, optional): Name of the parameter. Defaults to "".
#             descp (str, optional): Quick description for hints. Defaults to "".
#             set (list, optional): List of tolerated values. If empty, no restriction.
#             units (str, optional): Units (dB, Hz...). Defaults to "N/A".
#             minv (float, optional): Minimum value tolerated. Defaults to 0.0.
#             maxv (float, optional): Maximum value tolerated. Defaults to 1.0.
#             initv (float, optional): Initial value (and default after restart). Defaults to 0.0.
#             stepv (float, optional): Resolution on the parameter value. Defaults to 0.001.
#         """

#         if len(set) and not all(isinstance(i, float) for i in set):
#             raise ValueError(
#                 "DSPModuleParameter %s : the set has values that are of improper type, expected <float>."
#                 % (name)
#             )

#         super().__init__(name, descp, set)
#         self._minv = minv
#         self._maxv = maxv
#         self._initv = initv
#         self._stepv = stepv
#         self._units = units
#         self.val = initv

#         return

#     def __repr__(self) -> str:
#         """Detailed information about the DSPModuleParameter.

#         Returns:
#             str: formatted information
#         """

#         if len(self._set) == 0:
#             return "%s (float, in range [%.4f : %.4f : %.4f] in %s) : %s" % (
#                 self._name,
#                 self._minv,
#                 self._stepv,
#                 self._maxv,
#                 self._units,
#                 self._description,
#             )
#         else:
#             str_set_values = " ".join(str(x) for x in self._set)
#             return "%s (float, values in the set [%s] in %s) : %s" % (
#                 self._name,
#                 str_set_values,
#                 self._units,
#                 self._description,
#             )

#     @property
#     def val(self) -> float:
#         return self._val

#     @val.setter
#     def val(self, v: float):
#         """Setter for the parameter value :
#         - check the validity of the candidate value
#         - apply callbacks attached to the parameter (typicially the configure() method of the DSPModule)
#         - forks behavior depending on set or range

#         Args:
#             v (float): candidate value
#         """

#         if not isinstance(v, float):
#             raise ValueError(
#                 "DSPModuleParameter <%s> SETTER : the candidate value has improper type, expected <float>."
#                 % (self._name)
#             )

#         reference = self.val

#         if len(self._set) != 0:
#             # check inclusion of the candidate value
#             if v in self._set:
#                 self._val = v
#         else:
#             # apply boundaries to the candidate value
#             self._val = np.clip(v, self._minv, self._maxv)

#             # round with given accuracy
#             self._val = np.round(self._val / self._stepv) * self._stepv

#         # call configure() function of plugins
#         if reference != self.val:
#             print(
#                 "DSPModuleParameter <%s> : value changed from %f to %f"
#                 % (self._name, reference, self.val)
#             )
#             for cb in self._callbacks:
#                 cb()
#         pass
