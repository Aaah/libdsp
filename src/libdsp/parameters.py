import numpy as np

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

    def __init__(self, name: str = "", descp: str = ""):
        """Initialisation of a DSPModuleParameter.

        Args:
            name (str, optional): name of the parameter. Defaults to "".
            descp (str, optional): quick description of the parameter for hints. Defaults to "".
        """
        self._val = 0.0
        self._name = name
        self._description = descp
        self._callbacks = []

        return

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, v):
        """Setter for the value of the parameter :
        - check for acceptable value (bounds, type...)
        - trigger attached callbacks (typically the configure() method of the DSPModule it is attached to)

        Args:
            v (_type_): candidate value
        """

        # memorize the value
        self._val = v

        # call configure() function of plugins
        for cb in self._callbacks:
            cb()
        pass


class DSPModuleParameterFloat(DSPModuleParameter):
    """
    A float parameter for DSPModule.
    """

    def __init__(
        self,
        name: str = "",
        descp: str = "",
        units: str = "N/A",
        minv: float = 0.0,
        maxv: float = 1.0,
        initv: float = 0.0,
        stepv: float = 0.001,
    ):
        """Initialisation of a float parameter for DSPModules.

        Args:
            name (str, optional): Name of the parameter. Defaults to "".
            descp (str, optional): Quick description for hints. Defaults to "".
            units (str, optional): Units (dB, Hz...). Defaults to "N/A".
            minv (float, optional): Minimum value tolerated. Defaults to 0.0.
            maxv (float, optional): Maximum value tolerated. Defaults to 1.0.
            initv (float, optional): Initial value (and default after restart). Defaults to 0.0.
            stepv (float, optional): Resolution on the parameter value. Defaults to 0.001.
        """

        super().__init__(name, descp)
        self._minv = minv
        self._maxv = maxv
        self._initv = initv
        self._stepv = stepv
        self._units = units
        self.val = initv

        return

    @property
    def val(self) -> float:
        return self._val

    @val.setter
    def val(self, v: float):
        """Setter for the parameter value :
        - check the validity of the candidate value
        - apply callbacks attached to the parameter (typicially the configure() method of the DSPModule)

        Args:
            v (float): candidate value
        """

        # apply boundaries to the candidate value
        old_val = self.val
        self._val = np.clip(v, self._minv, self._maxv)

        print("value changed from %f to %f" % (old_val, self.val))

        # call configure() function of plugins
        for cb in self._callbacks:
            cb()
        pass


# class DSPModuleParameterString(DSPModuleParameter):
#     def __init__(self, name: str = "", descp: str = "", fmt: str = "", initv: str = ""):

#         super().__init__(name, descp)
#         self._initv = initv  # initial value
#         self._fmt = fmt  # format of the string
#         self.val = initv

#         return

#     @property
#     def val(self):
#         return self._val

#     @val.setter
#     def val(self, v):

#         # todo : apply regexp to verify the format ?
#         # how to force the writing %d.%d.%d.%d:%d (in gui), which is different than checking '^[0-9]{3}\.[0-9]{3}\.[0-9]{3}\.[0-9]{3}\:.[0-9]{3}$' ?
#         self._val = str(v)

#         # call configure() function of plugins
#         for cb in self._callbacks:
#             cb()
#         pass
