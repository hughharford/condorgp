from deap import gp
import numpy
import random
import operator
import math
from datetime import timedelta

from decimal import Decimal

from nautilus_trader.examples.strategies.ema_cross import EMACrossConfig
from nautilus_trader.test_kit.providers import TestInstrumentProvider
from nautilus_trader.model.identifiers import Venue
from nautilus_trader.model.identifiers import InstrumentId

import logging

class GpPsets:
    ''' Provides population sets (psets) for CondorGP '''
    def __init__(self, custom_funcs):
        self.cfs = custom_funcs

    def get_named_pset(self, named_pset):
        try:
            return eval('self.get_' + named_pset + '()')
        except BaseException as e:
            print("GpPsets ERROR: " + str(e))
            return None

    # def get_default_untyped(self):
    #      # basic untyped deap.gp.PrimitiveSet:
    #     self.default_untyped = gp.PrimitiveSet("default_untyped", 1)
    #     self.default_untyped.addPrimitive(numpy.add, 2, name="vadd")
    #     self.default_untyped.addPrimitive(numpy.subtract, 2, name="vsub")
    #     self.default_untyped.addPrimitive(numpy.multiply, 2, name="vmul")
    #     self.default_untyped.addPrimitive(numpy.negative, 1, name="vneg")
    #     self.default_untyped.addPrimitive(numpy.cos, 1, name="vcos")
    #     self.default_untyped.addPrimitive(numpy.sin, 1, name="vsin")
    #     self.default_untyped.addEphemeralConstant(
    #                                             "number78",
    #                                             78)
    #     self.default_untyped.renameArguments(ARG0='x')
    #     return self.default_untyped

    def get_test_pset5a(self):
        ''' test_pset5a '''
        self.test5a = gp.PrimitiveSet("test_pset5a", 0)
        self.test5a.addPrimitive(numpy.multiply, 2, name="vmul")
        return self.test5a

    def get_test_pset5b(self):
        ''' test_pset5b '''
        self.test5b = gp.PrimitiveSet("test_pset5b", 0)
        self.test5b.addPrimitive(numpy.add, 2, name="vadd")
        self.test5b.addPrimitive(print, 1, name="print")
        self.test5b.addTerminal("***_***_***", "3x3")
        return self.test5b

    # def get_test_pset5c(self):
    #     ''' test_pset5c '''
    #     self.test5c = gp.PrimitiveSet("test_pset5c", 1)
    #     self.test5c.addPrimitive(logging.info, 1, name="logging.info")
    #     self.test5c.renameArguments(ARG0='x0')
    #     return self.test5c

    # def get_test_pset7aTyped(self):
    #     ''' test_pset_7aTyped '''
    #     self.test7a = gp.PrimitiveSetTyped("test_pset_7aTyped",[object],str)
    #     self.test7a.addTerminal(1, int)
    #     self.test7a.addTerminal(0, int)
    #     self.test7a.addPrimitive(self.cfs.get_alpha_model_A,[int],str)
    #     self.test7a.addPrimitive(self.cfs.get_alpha_model_B,[int],str)
    #     self.test7a.addPrimitive(self.cfs.get_alpha_model_C,[int],str)
    #     self.test7a.addPrimitive(self.cfs.get_alpha_model_D,[int],str)
    #     # dummy int primitive, with name "" to avoid func call
    #     self.test7a.addPrimitive(self.cfs.double,[int],int, "")

    #     return self.test7a

    def get_naut_pset_02_adf(self):
        ''' naut_pset_02_adf

        # looking to add simple ADF to integer choice and evolve:

        # def get_config_strategy(self):
        #     config = EMACrossConfig(
        #         instrument_id=str(self.instrument.id),
        #         bar_type=self.bar_type,
        #         trade_size=Decimal(1_000_000),
        #         fast_ema_period=100,
        #         slow_ema_period=200,
        #         )
        #     return config
        '''

        # ADF0 pset ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        self.adfset0 = gp.PrimitiveSetTyped("ADF0", [LittleInt], LittleInt, "ARG")
        self.adfset0.addPrimitive(operator.add, [LittleInt, LittleInt], LittleInt)
        self.adfset0.addPrimitive(operator.sub, [LittleInt, LittleInt], LittleInt)
        self.adfset0.addPrimitive(operator.mul, [LittleInt], LittleInt)
        # self.adfset0.addPrimitive(protectedDiv, [LittleInt, LittleInt], LittleInt)
        self.adfset0.addPrimitive(operator.neg, [LittleInt], LittleInt)
        # self.adfset0.addTerminal(10, LittleInt)

        # self.adfset0.addPrimitive(math.cos, 1)
        # self.adfset0.addPrimitive(math.sin, 1)
        # self.adfset0.addADF(adfset1)
        # self.adfset0.addADF(adfset2)
        # self.adfset0.renameArguments(ARG0='x0')
        # self.adfset0.renameArguments(ARG1='y0')

        # MAIN pset ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        bar_type = "AUD/USD.SIM-1-MINUTE-MID-INTERNAL"
        bar_type2 = "AUD/USD.SIM-1-MINUTE-MID-INTERNAL"
        self.SIM = Venue("SIM")
        inst = TestInstrumentProvider.default_fx_ccy("AUD/USD", self.SIM)
        inst2 = TestInstrumentProvider.default_fx_ccy("AUD/USD",self.SIM)

        # a first basic primitive set for strongly typed GP using Nautilus
        self.pset = gp.PrimitiveSetTyped("CGPNAUT02",
                                         [], EMACrossConfig, "ARG")
        # primary primitive, to enable function
        self.pset.addPrimitive(EMACrossConfig,
                               [StrInstr, StrBar, Decimal, LittleInt, BigInt],
                               EMACrossConfig)
        # first pset terminals:
        self.pset.addTerminal(StrInstr(inst.id), StrInstr)
        self.pset.addTerminal(StrInstr(inst2.id), StrInstr)
        self.pset.addTerminal(bar_type, StrBar)
        self.pset.addTerminal(bar_type2, StrBar)
        self.pset.addTerminal(10, LittleInt)
        self.pset.addTerminal(20, LittleInt)
        self.pset.addTerminal(30, LittleInt)
        self.pset.addTerminal(40, LittleInt)
        self.pset.addTerminal(50, BigInt)
        self.pset.addTerminal(100, BigInt)
        self.pset.addTerminal(200, BigInt)
        self.pset.addTerminal(1_000_000, int)
        self.pset.addTerminal(2_000_000, int)
        # below here were added to allow DEAP to populate
        self.pset.addPrimitive(Decimal, [Decimal], Decimal)
        self.pset.addPrimitive(str, [str], str)
        self.pset.addPrimitive(int, [int], int)
        self.pset.addTerminal(Decimal(1_000_000), Decimal)
        self.pset.addTerminal("EMACrossConfig", EMACrossConfig)
        # using specified int and str classes to reduce degress of freedom
        self.pset.addPrimitive(BigInt, [BigInt], BigInt)
        self.pset.addPrimitive(LittleInt, [LittleInt], LittleInt)
        self.pset.addPrimitive(str, [StrInstr], StrInstr)
        self.pset.addPrimitive(str, [StrBar], StrBar)
        # add ADF:
        self.pset.addADF(self.adfset0)

        self.psets = (self.pset, self.adfset0)

        return self.psets



    def get_naut_pset_01(self):
        ''' naut_pset_01

        # successfully evolves:

        # def get_config_strategy(self):
        #     config = EMACrossConfig(
        #         instrument_id=str(self.instrument.id),
        #         bar_type=self.bar_type,
        #         trade_size=Decimal(1_000_000),
        #         fast_ema_period=100,
        #         slow_ema_period=200,
        #         )
        #     return config
        '''
        bar_type = "AUD/USD.SIM-1-MINUTE-MID-INTERNAL"
        bar_type2 = "AUD/USD.SIM-1-MINUTE-MID-INTERNAL"
        self.SIM = Venue("SIM")
        inst = TestInstrumentProvider.default_fx_ccy("AUD/USD", self.SIM)
        inst2 = TestInstrumentProvider.default_fx_ccy("AUD/USD",self.SIM)
        # a first basic primitive set for strongly typed GP using Nautilus
        self.pset = gp.PrimitiveSetTyped("CGPNAUT01",
                                         [], EMACrossConfig, "ARG")
        # primary primitive, to enable function
        self.pset.addPrimitive(EMACrossConfig,
                               [StrInstr, StrBar, Decimal, LittleInt, BigInt],
                               EMACrossConfig)
        # first pset terminals:
        self.pset.addTerminal(StrInstr(inst.id), StrInstr)
        self.pset.addTerminal(StrInstr(inst2.id), StrInstr)
        self.pset.addTerminal(bar_type, StrBar)
        self.pset.addTerminal(bar_type2, StrBar)
        self.pset.addTerminal(10, LittleInt)
        self.pset.addTerminal(20, LittleInt)
        self.pset.addTerminal(30, LittleInt)
        self.pset.addTerminal(40, LittleInt)
        self.pset.addTerminal(50, BigInt)
        self.pset.addTerminal(100, BigInt)
        self.pset.addTerminal(200, BigInt)
        self.pset.addTerminal(1_000_000, int)
        self.pset.addTerminal(2_000_000, int)
        # below here were added to allow DEAP to populate
        self.pset.addPrimitive(Decimal, [Decimal], Decimal)
        self.pset.addPrimitive(str, [str], str)
        self.pset.addPrimitive(int, [int], int)
        self.pset.addTerminal(Decimal(1_000_000), Decimal)
        self.pset.addTerminal("EMACrossConfig", EMACrossConfig)
        # using specified int and str classes to reduce degress of freedom
        self.pset.addPrimitive(BigInt, [BigInt], BigInt)
        self.pset.addPrimitive(LittleInt, [LittleInt], LittleInt)
        self.pset.addPrimitive(str, [StrInstr], StrInstr)
        self.pset.addPrimitive(str, [StrBar], StrBar)
        return self.pset

# Define new functions
def protectedDiv(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return 1

class StrInstr(str):
    def pass_method(self):
        pass

class StrBar(str):
    def pass_method(self):
        pass

class BigInt(int):
    def pass_method(self):
        pass

class LittleInt(int):
    def pass_method(self):
        pass

if __name__ == '__main__':
    pass

    # uncomment the below and run to have a look into a pset created above:

    from deap import gp
    from condorgp.factories.custom_funcs_factory import CustomFuncsFactory
    cf = CustomFuncsFactory()
    gp_custom_funcs = cf.get_gp_custom_functions()
    gpp = GpPsets(gp_custom_funcs)
    pset_and_adf = gpp.get_named_pset('naut_pset_02_adf')
    print(f"{type(pset_and_adf[0])} named: {pset_and_adf[0].name}")
    print(f"{type(pset_and_adf[1])} named: {pset_and_adf[1].name}")

    # # print('looking at terminals:')
    # print('count of terminals: ', one.terms_count,
    #       ' ... n.b. always one more than actual, due to base class')
    # term_keys = list(one.terminals.keys())
    # print(term_keys)

    # list_terminals = one.terminals.get(term_keys[0])
    # print(list_terminals)

    # prim_names = list(one.context.keys())
    # print(prim_names)
