from deap import gp
import numpy
import random
import operator
import math
from datetime import timedelta

from condorgp.util.log import CondorLogger
# from AlgorithmImports import *
from QuantConnect.Algorithm.Framework.Alphas import *
    # RsiAlphaModel, MacdAlphaModel, EmaCrossAlphaModel, BasePairsTradingAlphaModel
from QuantConnect import Resolution
from QuantConnect.Indicators import *
from QuantConnect.Algorithm import QCAlgorithm
# fails: from QuantConnnect.Common import *
import clr
from clr import AddReference


class pt_alpha():
    def __init__(self) -> None:
        # see Lean/Algorithm.Framework/Alphas
        # self.MACD = MacdAlphaModel(fastPeriod = 12,
        #         slowPeriod = 26,
        #         signalPeriod = 9,
        #         movingAverageType = MovingAverageType.Exponential,
        #         resolution = Resolution.Daily)
        self.EMA = EmaCrossAlphaModel(fastPeriod = 12,
                slowPeriod = 26,
                resolution = Resolution.Daily)
        self.BPTA = BasePairsTradingAlphaModel(
                lookback = 1,
                resolution = Resolution.Daily,
                threshold = 1)
        # for later...
        # self.BPTA_0 = BasePairsTradingAlphaModel()

class pt_method():
    # def __init__(self) -> None:
    #     # takes IAlphaModel or just AlphaModel?
    #     self.AddAlpha = QCAlgorithm.AddAlpha() # P, ret: AlphaModel
    #     self.SetAlpha = QCAlgorithm.SetAlpha(RsiAlphaModel()) # T, None
    AddAlpha = QCAlgorithm.AddAlpha() # P, ret: AlphaModel


class pt_indicator():
    def __init__(self):
        self.sma = QCAlgorithm.SMA("SPY", 60, Resolution.Minute())

class pt_resolution():
    def __init__(self):
        self.Daily = Resolution.Daily
        self.Hour = Resolution.Hour
        self.Minute = Resolution.Minute
        self.Hour_0 = timedelta(minutes=60)
        # self.x = Resolution(4)


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
class GpPsets:
    def __init__(self, custom_funcs):
        self.cfs = custom_funcs
        self.log = CondorLogger().get_logger()
        # self.pt_method = pt_method()
        self.pt_alpha = pt_alpha()
        # self.pt_indicator = pt_indicator()
        self.pt_resolution = pt_resolution()

    def get_named_pset(self, named_pset):
        try:
            return eval('self.get_' + named_pset + '()')
        except BaseException as e:
            print("GpPsets ERROR: " + str(e))
            return None

    def get_test_pset8aTyped(self):
        '''test_pset8aTyped'''
        self.test8a = gp.PrimitiveSetTyped("test_pset8aTyped",[pt_method],None)

        # pt_method (P and T)
        # EXPECT TO CUT THIS OUT AND REPLACE pset in-type with pt_alpha
        self.test8a.addPrimitive(
            pt_method.AddAlpha, [pt_alpha], pt_method)
        self.test8a.addTerminal(
            QCAlgorithm.SetAlpha(RsiAlphaModel()),
            [pt_method],
            name = "self.SetAlpha(RsiAlphaModel()")

        # pt_alpha (P and T)
        self.test8a.addTerminal(pt_alpha.EMA, pt_alpha)
        self.test8a.addTerminal(pt_alpha.MACD, pt_alpha)
        self.test8a.addTerminal(pt_alpha.BPTA, pt_alpha)
        self.test8a.addPrimitive(
            EmaCrossAlphaModel, [int, int, Resolution], pt_alpha)
        # self.test8a.addPrimitive()

        # pt_resolution (P and T)
        self.test8a.addPrimitive(Resolution, str)
        self.test8a.addTerminal(Resolution.Hour, Resolution)
        self.test8a.addTerminal(Resolution.Minute, Resolution)
        self.test8a.addTerminal(Resolution.Second, Resolution)

        self.test8a.addTerminal("Hourly", str, name=".Hour")
        self.test8a.addTerminal("Minute", str, name=".Minute")

        # int (P and T)
        self.test8a.addTerminal(1, int)
        self.test8a.addTerminal(2, int)
        self.test8a.addTerminal(3, int)
        self.test8a.addTerminal(5, int)
        self.test8a.addTerminal(10, int)
        self.test8a.addTerminal(20, int)
        self.test8a.addPrimitive(operator.add, [int, int], int)
        self.test8a.addPrimitive(operator.sub, [int, int], int)
        self.test8a.addPrimitive(operator.mul, [int, int], int)
        self.test8a.addPrimitive(self.cfs.protectedDiv, [int, int], int)
        self.test8a.addPrimitive(operator.neg, [int], int)

        return self.test823
    def get_default_untyped(self):
         # basic untyped deap.gp.PrimitiveSet:
        self.default_untyped = gp.PrimitiveSet("DEFAULT UNTYPED", 1)
        self.default_untyped.addPrimitive(numpy.add, 2, name="vadd")
        self.default_untyped.addPrimitive(numpy.subtract, 2, name="vsub")
        self.default_untyped.addPrimitive(numpy.multiply, 2, name="vmul")
        self.default_untyped.addPrimitive(numpy.negative, 1, name="vneg")
        self.default_untyped.addPrimitive(numpy.cos, 1, name="vcos")
        self.default_untyped.addPrimitive(numpy.sin, 1, name="vsin")
        self.default_untyped.addEphemeralConstant(
                                                "rand101",
                                                lambda: random.randint(-1,1))
        self.default_untyped.renameArguments(ARG0='x')
        return self.default_untyped

    def get_experimental_untyped_pset(self):

        self.experimental_untyped = gp.PrimitiveSet("exp_untyped", 0)
        self.experimental_untyped.addPrimitive(numpy.cos, 1, name="vcos")
        return self.experimental_untyped


    def get_test_base_pset(self):
        ''' test base pset '''
        self.test_base = gp.PrimitiveSet("test_base_pset", 1)
        self.test_base.addPrimitive(numpy.cos, 1, name="vcos")
        self.test_base.addPrimitive(numpy.sin, 1, name="vsin")
        return self.test_base

    def get_test_pset5a(self):
        ''' test pset 5a '''
        self.test5a = gp.PrimitiveSet("test pset 5a", 0)
        self.test5a.addPrimitive(numpy.multiply, 2, name="vmul")
        return self.test5a

    def get_test_pset5b(self):
        ''' test pset 5b '''
        self.test5b = gp.PrimitiveSet("test pset 5b", 0)
        self.test5b.addPrimitive(numpy.add, 2, name="vadd")
        self.test5b.addPrimitive(print, 1, name="print")
        self.test5b.addTerminal("***_***_***", "3x3")
        return self.test5b

    def get_test_pset5c(self):
        ''' test pset 5c '''
        self.test5c = gp.PrimitiveSet("test pset 5c", 1)
        self.test5c.addPrimitive(self.log.info, 1, name="self.log.info")
        self.test5c.renameArguments(ARG0='x0')
        return self.test5c

    def get_test_pset5d(self):
        ''' test pset 5d '''
        self.test5d = gp.PrimitiveSet("test pset 5d", 1)
        self.test5d.addPrimitive(self.log.info, 1, name="self.log.info")
        self.test5d.renameArguments(ARG0='x0')
        return self.test5d

    def get_test_pset6a(self):
        ''' test pset 6a '''
        self.test6a = gp.PrimitiveSet("test pset 6a", 0)
        self.test6a.addTerminal(1)
        self.test6a.addPrimitive(self.cfs.get_alpha_model_A,1)
        return self.test6a

    def get_test_pset6b(self):
        ''' test pset 6b '''
        self.test6b = gp.PrimitiveSet("test pset 6b", 0)
        self.test6b.addTerminal(1)
        self.test6b.addPrimitive(self.cfs.get_alpha_model_B,1)
        return self.test6b


    def get_test_pset7aTyped(self):
        ''' test pset 7aTyped '''
        self.test7a = gp.PrimitiveSetTyped("test pset 7aTyped",[object],str)
        self.test7a.addTerminal(1, int)
        self.test7a.addTerminal(0, int)
        self.test7a.addPrimitive(self.cfs.get_alpha_model_A,[int],str)
        self.test7a.addPrimitive(self.cfs.get_alpha_model_B,[int],str)
        self.test7a.addPrimitive(self.cfs.get_alpha_model_C,[int],str)
        self.test7a.addPrimitive(self.cfs.get_alpha_model_D,[int],str)
        # dummy int primitive, with name "" to avoid func call
        self.test7a.addPrimitive(self.cfs.double,[int],int, "")

        return self.test7a


    def get_adf2(self):
        self.adfset2 = gp.PrimitiveSet("ADF2", 2)
        self.adfset2.addPrimitive(operator.add, 2)
        self.adfset2.addPrimitive(operator.sub, 2)
        self.adfset2.addPrimitive(operator.mul, 2)
        self.adfset2.addPrimitive(self.cfs.protectedDiv, 2)
        self.adfset2.addPrimitive(operator.neg, 1)
        self.adfset2.addPrimitive(math.cos, 1)
        self.adfset2.addPrimitive(math.sin, 1)
        self.adfset2.renameArguments(ARG0='x2')
        self.adfset2.renameArguments(ARG1='y2')
        return self.adfset2

    def get_adf1(self):
        self.adfset1 = gp.PrimitiveSet("ADF1", 2)
        self.adfset1.addPrimitive(operator.add, 2)
        self.adfset1.addPrimitive(operator.sub, 2)
        self.adfset1.addPrimitive(operator.mul, 2)
        self.adfset1.addPrimitive(self.cfs.protectedDiv, 2)
        self.adfset1.addPrimitive(operator.neg, 1)
        self.adfset1.addPrimitive(math.cos, 1)
        self.adfset1.addPrimitive(math.sin, 1)
        self.adfset1.addADF(self.get_adf2())
        self.adfset1.renameArguments(ARG0='x1')
        self.adfset1.renameArguments(ARG1='y1')
        return self.adfset1

    def get_adf0(self):
        self.adfset0 = gp.PrimitiveSet("ADF0", 2)
        self.adfset0.addPrimitive(operator.add, 2)
        self.adfset0.addPrimitive(operator.sub, 2)
        self.adfset0.addPrimitive(operator.mul, 2)
        self.adfset0.addPrimitive(self.cfs.protectedDiv, 2)
        self.adfset0.addPrimitive(operator.neg, 1)
        self.adfset0.addPrimitive(math.cos, 1)
        self.adfset0.addPrimitive(math.sin, 1)
        self.adfset0.addADF(self.get_adf1())
        self.adfset0.addADF(self.get_adf2())
        self.adfset0.renameArguments(ARG0='x0')
        self.adfset0.renameArguments(ARG1='y0')
        return self.adfset0

if __name__ == '__main__':
    pass

    # uncomment the below and run to have a look into a pset created above:

    from deap import gp
    from condorgp.factories.custom_funcs_factory import CustomFuncsFactory
    cf = CustomFuncsFactory()
    gp_custom_funcs = cf.get_gp_custom_functions()
    gpp = GpPsets(gp_custom_funcs)
    one = gpp.get_named_pset('test_psetC')
    # set_pset('test_psetC_untyped')
    print(type(one))

    print('looking at terminals:')
    print('count of terminals: ', one.terms_count,
          ' ... n.b. always one more than actual, due to base class')
    term_keys = list(one.terminals.keys())
    print(term_keys)
    list_terminals = one.terminals.get(term_keys[0])
    print(list_terminals)

    prim_names = list(one.context.keys())
    print(prim_names)
