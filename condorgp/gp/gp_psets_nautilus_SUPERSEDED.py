from deap import gp
import numpy
import random
import operator
import math
import itertools
from datetime import timedelta
from decimal import Decimal

from nautilus_trader.examples.strategies.ema_cross import EMACrossConfig
from nautilus_trader.test_kit.providers import TestInstrumentProvider
from nautilus_trader.model.identifiers import Venue

import logging
from condorgp.util.log import CondorLogger

class GpPsetsNautilus:

    def __init__(self, custom_funcs):
        self.cfs = custom_funcs

    def get_named_pset(self, named_pset):
        try:
            return eval('self.get_' + named_pset + '()')
        except BaseException as e:
            print("GpPsets ERROR: " + str(e))
            return None

    def get_naut_pset_01(self):
        ''' naut_pset_01 '''
        self.bar_type = "AUD/USD.SIM-1-MINUTE-MID-INTERNAL"
        self.SIM = Venue("SIM")
        self.instrument = TestInstrumentProvider.default_fx_ccy(
            "AUD/USD",
            self.SIM)
        # a first basic primitive set for strongly typed GP using Nautilus
        self.pset = gp.PrimitiveSetTyped("CGPNAUT01",
                                         [], EMACrossConfig, "ARG")

        # first pset terminals:
        self.pset.addTerminal(str(self.instrument.id), str)
        self.pset.addTerminal(self.bar_type, str)
        self.pset.addTerminal(100, int)
        self.pset.addTerminal(200, int)
        self.pset.addTerminal(1_000_000, int)

        self.pset.addPrimitive(Decimal, [int], Decimal)
        self.pset.addPrimitive(EMACrossConfig,
                               [str, str, Decimal, int, int],
                               EMACrossConfig)

        # below here were added to allow DEAP to populate
        self.pset.addPrimitive(str, [int], str)
        self.pset.addPrimitive(int, [int], int)

        self.pset.addTerminal(Decimal(1_000_000), Decimal)
        self.pset.addTerminal("EMACrossConfig", EMACrossConfig)


        return self.pset

        #   def get_config_strategy_without_full_declaration(self):
        #     config = EMACrossConfig(
        #         str(self.instrument.id),
        #         self.bar_type,
        #         Decimal(1_000_000),
        #         100,
        #         200,
        #         )
        #     return config

        # first attempt at Nautilus - looking to evolve the above

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
