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
from condorgp.util.log import CondorLogger

# class pt_alpha():
#     '''
#     very Lean focused and coupled,
#     must adjust style as well as backtester
#     '''
#     def __init__(self) -> None:
#         pass
#         # # see Lean/Algorithm.Framework/Alphas
#         # self.MACD = MacdAlphaModel(fastPeriod = 12,
#         #         slowPeriod = 26,
#         #         signalPeriod = 9,
#         #         movingAverageType = MovingAverageType.Exponential,
#         #         resolution = Resolution.Daily)
#         # self.EMA = EmaCrossAlphaModel(fastPeriod = 12,
#         #         slowPeriod = 26,
#         #         resolution = Resolution.Daily)
#         # self.BPTA = BasePairsTradingAlphaModel(
#         #         lookback = 1,
#         #         resolution = Resolution.Daily,
#         #         threshold = 1)
#         # for later...
#         # self.BPTA_0 = BasePairsTradingAlphaModel()

# class pt_method():
#     '''
#     very Lean focused and coupled,
#     must adjust style as well as backtester
#     '''
#     def __init__(self) -> None:
#         # takes IAlphaModel or just AlphaModel?
#     #     self.AddAlpha = QCAlgorithm.AddAlpha() # P, ret: AlphaModel
#     #     self.SetAlpha = QCAlgorithm.SetAlpha(RsiAlphaModel()) # T, None
#     # # AddAlpha = QCAlgorithm.AddAlpha() # P, ret: AlphaModel
#         pass

# # class pt_indicator():
# #     def __init__(self):
# #         pass
# #         # self.sma = QCAlgorithm.SMA("SPY", 60, Resolution.Minute())

# class pt_resolution():
#     '''
#     very Lean focused and coupled,
#     must adjust style as well as backtester
#     '''
#     def __init__(self):
#         pass
#         # self.Daily = Resolution.Daily
#         # self.Hour = Resolution.Hour
#         # self.Minute = Resolution.Minute
#         # self.Hour_0 = timedelta(minutes=60)
#         # # self.x = Resolution(4)


# # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
class GpPsets:
    def __init__(self, custom_funcs):
        self.cfs = custom_funcs
        # self.log = CondorLogger().get_logger()
        # self.pt_method = pt_method()
        # self.pt_alpha = pt_alpha()
        # self.pt_indicator = pt_indicator()
        # self.pt_resolution = pt_resolution()

    def get_named_pset(self, named_pset):
        try:
            return eval('self.get_' + named_pset + '()')
        except BaseException as e:
            print("GpPsets ERROR: " + str(e))
            return None

    # def get_test_pset8aTyped(self):
    #     '''test_pset8aTyped'''
    #     self.test8a = gp.PrimitiveSetTyped("test_pset8aTyped",[pt_method],None)
    #                                                     # aiming for pt_method

    #     # pt_method (P and T)
    #     # EXPECT TO CUT THIS OUT AND REPLACE pset in-type with pt_alpha
    #     # self.test8a.addPrimitive(
    #     #     pt_method.AddAlpha, [pt_alpha], pt_method)

    #     # TAKEN OUT WHILE TESTING pythonnet...
    #     # self.test8a.addTerminal(
    #     #      QCAlgorithm.SetAlpha(RsiAlphaModel()),
    #     #                         [pt_method],
    #     #                         name = "self.SetAlpha(RsiAlphaModel()")


    def get_default_untyped(self):
         # basic untyped deap.gp.PrimitiveSet:
        self.default_untyped = gp.PrimitiveSet("default_untyped", 1)
        self.default_untyped.addPrimitive(numpy.add, 2, name="vadd")
        self.default_untyped.addPrimitive(numpy.subtract, 2, name="vsub")
        self.default_untyped.addPrimitive(numpy.multiply, 2, name="vmul")
        self.default_untyped.addPrimitive(numpy.negative, 1, name="vneg")
        self.default_untyped.addPrimitive(numpy.cos, 1, name="vcos")
        self.default_untyped.addPrimitive(numpy.sin, 1, name="vsin")
        self.default_untyped.addEphemeralConstant(
                                                "number78",
                                                78)
        self.default_untyped.renameArguments(ARG0='x')
        return self.default_untyped

    def get_experimental_untyped_pset(self):

        self.experimental_untyped = gp.PrimitiveSet("exp_untyped", 0)
        self.experimental_untyped.addPrimitive(numpy.cos, 1, name="vcos")
        return self.experimental_untyped


    def get_test_base_pset(self):
        ''' test_base_pset '''
        self.test_base = gp.PrimitiveSet("test_base_pset", 1)
        self.test_base.addPrimitive(numpy.cos, 1, name="vcos")
        self.test_base.addPrimitive(numpy.sin, 1, name="vsin")
        return self.test_base

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

    def get_test_pset5c(self):
        ''' test_pset5c '''
        self.test5c = gp.PrimitiveSet("test_pset5c", 1)
        self.test5c.addPrimitive(logging.info, 1, name="logging.info")
        self.test5c.renameArguments(ARG0='x0')
        return self.test5c

    def get_test_pset5d(self):
        ''' test_pset5d '''
        self.test5d = gp.PrimitiveSet("test_pset5d", 1)
        self.test5d.addPrimitive(logging.info, 1, name="logging.info")
        self.test5d.renameArguments(ARG0='x0')
        return self.test5d

    def get_test_pset6a(self):
        ''' test_pset6a '''
        self.test6a = gp.PrimitiveSet("test_pset6a", 0)
        self.test6a.addTerminal(1)
        self.test6a.addPrimitive(self.cfs.get_alpha_model_A,1)
        return self.test6a

    def get_test_pset6b(self):
        ''' test_pset6b '''
        self.test6b = gp.PrimitiveSet("test_pset6b", 0)
        self.test6b.addTerminal(1)
        self.test6b.addPrimitive(self.cfs.get_alpha_model_B,1)
        return self.test6b

    def get_test_pset7aTyped(self):
        ''' test_pset_7aTyped '''
        self.test7a = gp.PrimitiveSetTyped("test_pset_7aTyped",[object],str)
        self.test7a.addTerminal(1, int)
        self.test7a.addTerminal(0, int)
        self.test7a.addPrimitive(self.cfs.get_alpha_model_A,[int],str)
        self.test7a.addPrimitive(self.cfs.get_alpha_model_B,[int],str)
        self.test7a.addPrimitive(self.cfs.get_alpha_model_C,[int],str)
        self.test7a.addPrimitive(self.cfs.get_alpha_model_D,[int],str)
        # dummy int primitive, with name "" to avoid func call
        self.test7a.addPrimitive(self.cfs.double,[int],int, "")

        return self.test7a


#     def get_adf2(self):
#         self.adfset2 = gp.PrimitiveSet("ADF2", 2)
#         self.adfset2.addPrimitive(operator.add, 2)
#         self.adfset2.addPrimitive(operator.sub, 2)
#         self.adfset2.addPrimitive(operator.mul, 2)
#         self.adfset2.addPrimitive(self.cfs.protectedDiv, 2)
#         self.adfset2.addPrimitive(operator.neg, 1)
#         self.adfset2.addPrimitive(math.cos, 1)
#         self.adfset2.addPrimitive(math.sin, 1)
#         self.adfset2.renameArguments(ARG0='x2')
#         self.adfset2.renameArguments(ARG1='y2')
#         return self.adfset2

#     def get_adf1(self):
#         self.adfset1 = gp.PrimitiveSet("ADF1", 2)
#         self.adfset1.addPrimitive(operator.add, 2)
#         self.adfset1.addPrimitive(operator.sub, 2)
#         self.adfset1.addPrimitive(operator.mul, 2)
#         self.adfset1.addPrimitive(self.cfs.protectedDiv, 2)
#         self.adfset1.addPrimitive(operator.neg, 1)
#         self.adfset1.addPrimitive(math.cos, 1)
#         self.adfset1.addPrimitive(math.sin, 1)
#         self.adfset1.addADF(self.get_adf2())
#         self.adfset1.renameArguments(ARG0='x1')
#         self.adfset1.renameArguments(ARG1='y1')
#         return self.adfset1

#     def get_adf0(self):
#         self.adfset0 = gp.PrimitiveSet("ADF0", 2)
#         self.adfset0.addPrimitive(operator.add, 2)
#         self.adfset0.addPrimitive(operator.sub, 2)
#         self.adfset0.addPrimitive(operator.mul, 2)
#         self.adfset0.addPrimitive(self.cfs.protectedDiv, 2)
#         self.adfset0.addPrimitive(operator.neg, 1)
#         self.adfset0.addPrimitive(math.cos, 1)
#         self.adfset0.addPrimitive(math.sin, 1)
#         self.adfset0.addADF(self.get_adf1())
#         self.adfset0.addADF(self.get_adf2())
#         self.adfset0.renameArguments(ARG0='x0')
#         self.adfset0.renameArguments(ARG1='y0')
#         return self.adfset0

    def get_naut_pset_01(self):
        ''' naut_pset_01 '''
        bar_type = "AUD/USD.SIM-1-MINUTE-MID-INTERNAL"
        bar_type2 = "AUD/USD.SIM-1-MINUTE-MID-INTERNAL"
        bar_type3 = "AUD/USD.SIM-1-MINUTE-MID-INTERNAL"

        self.SIM = Venue("SIM")
        inst = TestInstrumentProvider.default_fx_ccy("AUD/USD", self.SIM)
        inst2 = TestInstrumentProvider.default_fx_ccy("AUD/USD",self.SIM)
        inst3 = TestInstrumentProvider.default_fx_ccy("AUD/USD",self.SIM)
        # print(f"type(instrument) = {type(instrument)}")
        # print(f"type(instrument.id) = {type(instrument.id)}")
        # print(f"type(str(instrument.id)) = {type(str(instrument.id))}")
        print(f"str(instrument.id) = {str(inst.id)}")

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
        self.pset.addTerminal(StrInstr(inst3.id), StrInstr)

        self.pset.addTerminal(bar_type, StrBar)
        self.pset.addTerminal(bar_type2, StrBar)
        self.pset.addTerminal(bar_type3, StrBar)

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

        # def get_config_strategy(self):
        #     config = EMACrossConfig(
        #         instrument_id=str(self.instrument.id),
        #         bar_type=self.bar_type,
        #         trade_size=Decimal(1_000_000),
        #         fast_ema_period=100,
        #         slow_ema_period=200,
        #         )
        #     return config

        # first attempt at Nautilus - looking to evolve the above

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

    # from deap import gp
    # from condorgp.factories.custom_funcs_factory import CustomFuncsFactory
    # cf = CustomFuncsFactory()
    # gp_custom_funcs = cf.get_gp_custom_functions()
    # gpp = GpPsets(gp_custom_funcs)
    # one = gpp.get_named_pset('naut_pset_01')
    # # set_pset('test_psetC_untyped')
    # # print(type(one))

    # # print('looking at terminals:')
    # print('count of terminals: ', one.terms_count,
    #       ' ... n.b. always one more than actual, due to base class')
    # term_keys = list(one.terminals.keys())
    # print(term_keys)

    # list_terminals = one.terminals.get(term_keys[0])
    # print(list_terminals)

    # prim_names = list(one.context.keys())
    # print(prim_names)

    stringer = StrInstr("my test")
    print(stringer)
    print(len(stringer))
