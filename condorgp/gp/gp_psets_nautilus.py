from deap import gp
import numpy
import random
import operator
import math
import itertools
from datetime import timedelta

import logging
from condorgp.util.log import CondorLogger

class GpPsetsNautilus:

    def __init__(self, custom_funcs):
        self.cfs = custom_funcs

    def get_initial_naut_pset(self):
            # defined a new primitive set for strongly typed GP
        self.pset = gp.PrimitiveSetTyped("TYPED", itertools.repeat(float, 57), bool, "IN")

        # boolean operators
        self.pset.addPrimitive(operator.and_, [bool, bool], bool)
        self.pset.addPrimitive(operator.or_, [bool, bool], bool)
        self.pset.addPrimitive(operator.not_, [bool], bool)

        # floating point operators
        self.pset.addPrimitive(operator.add, [float,float], float)
        self.pset.addPrimitive(operator.sub, [float,float], float)
        self.pset.addPrimitive(operator.mul, [float,float], float)
        self.pset.addPrimitive(protectedDiv, [float,float], float)

        # logic operators
        self.pset.addPrimitive(operator.lt, [float, float], bool)
        self.pset.addPrimitive(operator.eq, [float, float], bool)
        self.pset.addPrimitive(if_then_else, [bool, float, float], float)

        # terminals
        self.pset.addEphemeralConstant("rand100", lambda: random.random() * 100, float)
        self.pset.addTerminal(False, bool)

# Define new functions
def protectedDiv(left, right):
    with numpy.errstate(divide='ignore',invalid='ignore'):
        x = numpy.divide(left, right)
        if isinstance(x, numpy.ndarray):
            x[numpy.isinf(x)] = 1
            x[numpy.isnan(x)] = 1
        elif numpy.isinf(x) or numpy.isnan(x):
            x = 1
    return x

# Define a new if-then-else function
def if_then_else(input, output1, output2):
    if input: return output1
    else: return output2
