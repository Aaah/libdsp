# import numpy as np
# from parameters import *

# __author__ = "Rémy VINCENT"
# __copyright__ = "Aaah"
# __license__ = "Copyright 2022"

# class DSPPlugin():
#     def __init__(self):

#         # parameters
#         self._name = ""
#         self._version = ""
#         self._author = ""
#         self._description = ""

#         # internals
#         self.__params = []
#         self.__inputs = []
#         self.__outputs = []

#         return

#     def add_parameter(self, param : DSPModuleParameter):

#         # check that the parameter does not exist yet
#         for p in self.__params:
#             if p._name == param._name:
#                 print("parameter with same name already exists, dismissing")
#                 return

#         # set the callback to the configure() function
#         param._callbacks.append(self.configure)

#         # add to list of parameters
#         self.__params.append(param)

#         return

#     def set_param(self, name : str, val):

#         for p in self.__params:
#             if p._name == name:
#                 p.val = val
#                 break

#         pass

#     def get_param(self, name : str):

#         for p in self.__params:
#             if p._name == name:
#                 return p.val

#         pass

#     # def add_input(self, input : DSPPluginIO):

#     #     # check that the input does not exist yet
#     #     for i in self.__inputs:
#     #         if i._name == input._name:
#     #             print("input with same name already exists, dismissing")
#     #             return

#     #     # add to list of inputs
#     #     self.__inputs.append(input)

#     #     pass

#     # def add_output(self, output : DSPPluginIO):

#     #     # check that the output does not exist yet
#     #     for i in self.__outputs:
#     #         if i._name == output._name:
#     #             print("output with same name already exists, dismissing")
#     #             return

#     #     # add to list of ouputs
#     #     self.__outputs.append(output)

#     #     pass

#     def run(self, *args, **kwds):
#         # actual signal processing
#         raise NotImplementedError("run method must be implemented.")

#     def configure(self):
#         # update internals based on parameters update, called everytime a parameter is changed
#         raise NotImplementedError("config method must be implemented.")


# class SimpleDSPPlugin(DSPPlugin):

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
#         # self.add_input( DSPPluginIOFloat("in") )
#         # self.add_output( DSPPluginIOFloat("out") )

#         pass

#     def configure(self):

#         # internal variables computed based on parameters
#         self._gain_lin = 10 ** (self.get_param("gain") / 20)

#         # other internal update
#         pass

#     def run(self, val):
#         return val * self._gain_lin
