from libdsp.parameters import *

__author__ = "Rémy VINCENT"
__copyright__ = "Aaah"
__license__ = "Copyright 2022"


class DSPModule:
    """Template class for DSP algorithms.
    Modules benefit from a set of parameters for their configuration : the configure() method is a callback triggered whenever a parameter is updated. Modules have a processing method called process() that can be called in an offline context (the whole data is passed to be processed) or in a streaming context (data is passed frame by frame).
    """

    def __init__(self, name=""):
        """Initialisation of the DSPModule instance.

        Args:
            name (str, optional): name of the instance. Defaults to "".
        """

        # parameters
        self._name = ""  # name of the instance
        self._version = ""  # version of the algorithm
        self._author = ""  # author of the algorithm
        self._description = ""  # short brief about the module

        # internals
        self.__params = []
        self.__inputs = []
        self.__outputs = []

        return

    def add_parameter(self, param: DSPModuleParameter):

        # check that the parameter does not exist yet
        for p in self.__params:
            if p._name == param._name:
                print("parameter with same name already exists, dismissing")
                return

        # set the callback to the configure() function
        param._callbacks.append(self.configure)

        # add to list of parameters
        self.__params.append(param)

        return

    def set_param(self, name: str, val):

        for p in self.__params:
            if p._name == name:
                p.val = val
                return

        print("no parameter found with the given name")

        pass

    def get_param(self, name: str):

        for p in self.__params:
            if p._name == name:
                return p.val

        print("no parameter found with the given name")

        pass

    # def add_input(self, input : DSPModuleIO):

    #     # check that the input does not exist yet
    #     for i in self.__inputs:
    #         if i._name == input._name:
    #             print("input with same name already exists, dismissing")
    #             return

    #     # add to list of inputs
    #     self.__inputs.append(input)

    #     pass

    # def add_output(self, output : DSPModuleIO):

    #     # check that the output does not exist yet
    #     for i in self.__outputs:
    #         if i._name == output._name:
    #             print("output with same name already exists, dismissing")
    #             return

    #     # add to list of ouputs
    #     self.__outputs.append(output)

    #     pass

    def process(self, *args, **kwds):
        # actual signal processing
        raise NotImplementedError("process method must be implemented.")

    def configure(self):
        # update internals based on parameters update, called everytime a parameter is changed
        raise NotImplementedError("config method must be implemented.")


# class SimpleDSPModule(DSPModule):

#     def __init__(self, name =""):

#         super().__init__()

#         # memorize the name of the instance
#         self._name = name
#         self._version = "0.1.0"
#         self._author = __author__
#         self._description = "A simple gain plugin"

#         # create parameters for the plugin
#         self.add_parameter( DSPModuleParameterFloat(name = "gain", units = "dB", minv = 0.0, maxv = 109.0) )
#         self.add_parameter( DSPModuleParameterFloat(name = "threshold", units = "Hz", minv = 0.0, maxv = 1000.0) )

#         # # create inputs and outputs
#         # self.add_input( DSPModuleIOFloat("in") )
#         # self.add_output( DSPModuleIOFloat("out") )

#         pass

#     def configure(self):

#         # internal variables computed based on parameters
#         self._gain_lin = 10 ** (self.get_param("gain") / 20)

#         # other internal update
#         pass

#     def run(self, val):
#         return val * self._gain_lin
