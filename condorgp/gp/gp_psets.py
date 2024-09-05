from deap import gp
import numpy
import random
import operator
import math
from datetime import timedelta

from decimal import Decimal

from condorgp.evaluation.gp_run_strat_base import GpRunStrategyBase
from condorgp.evaluation.gp_run_strat_base import GpRunStrategyBaseConfig
from condorgp.evaluation.gp_run_strat_inject import GpRunStrategyInject
from condorgp.evaluation.get_strategies import GetStrategies

from nautilus_trader.trading.strategy import Strategy

from nautilus_trader.examples.strategies.ema_cross import EMACrossConfig
from nautilus_trader.test_kit.providers import TestInstrumentProvider
from nautilus_trader.model.identifiers import Venue
from nautilus_trader.model.identifiers import InstrumentId
from nautilus_trader.model.instruments.currency_pair import CurrencyPair

import logging
import traceback

class GpPsets:
    ''' Provides population sets (psets) for CondorGP '''
    def __init__(self):
        pass

    def get_named_pset(self, named_pset):
        try:
            return eval('self.get_' + named_pset + '()')
        except BaseException as e:
            logging.error("GpPsets.get_named_pset ERROR: " + str(e))
            tb = ''.join(traceback.format_tb(e.__traceback__))
            logging.debug(f"GpPsets.get_named_pset: {tb}")
            return None

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

    def get_test_adf_symbreg_pset(self):
        ''' test_adf_symbreg_pset '''
                # Define new functions
        def protectedDiv(left, right):
            try:
                return left / right
            except ZeroDivisionError:
                return 1

        adfset2 = gp.PrimitiveSet("ADF2", 2)
        adfset2.addPrimitive(operator.add, 2)
        adfset2.addPrimitive(operator.sub, 2)
        adfset2.addPrimitive(operator.mul, 2)
        adfset2.addPrimitive(protectedDiv, 2)
        adfset2.addPrimitive(operator.neg, 1)
        adfset2.addPrimitive(math.cos, 1)
        adfset2.addPrimitive(math.sin, 1)

        adfset1 = gp.PrimitiveSet("ADF1", 2)
        adfset1.addPrimitive(operator.add, 2)
        adfset1.addPrimitive(operator.sub, 2)
        adfset1.addPrimitive(operator.mul, 2)
        adfset1.addPrimitive(protectedDiv, 2)
        adfset1.addPrimitive(operator.neg, 1)
        adfset1.addPrimitive(math.cos, 1)
        adfset1.addPrimitive(math.sin, 1)
        adfset1.addADF(adfset2)

        adfset0 = gp.PrimitiveSet("ADF0", 2)
        adfset0.addPrimitive(operator.add, 2)
        adfset0.addPrimitive(operator.sub, 2)
        adfset0.addPrimitive(operator.mul, 2)
        adfset0.addPrimitive(protectedDiv, 2)
        adfset0.addPrimitive(operator.neg, 1)
        adfset0.addPrimitive(math.cos, 1)
        adfset0.addPrimitive(math.sin, 1)
        adfset0.addADF(adfset1)
        adfset0.addADF(adfset2)

        pset = gp.PrimitiveSet("MAIN", 1)
        pset.addPrimitive(operator.add, 2)
        pset.addPrimitive(operator.sub, 2)
        pset.addPrimitive(operator.mul, 2)
        pset.addPrimitive(protectedDiv, 2)
        pset.addPrimitive(operator.neg, 1)
        pset.addPrimitive(math.cos, 1)
        pset.addPrimitive(math.sin, 1)
        # pset.addEphemeralConstant("rand101", lambda: random.randint(-1, 1))
        pset.addADF(adfset0)
        pset.addADF(adfset1)
        pset.addADF(adfset2)
        pset.renameArguments(ARG0='x')

        psets = (pset, adfset0, adfset1, adfset2)

        return psets

    def get_naut_pset_05_strategy(self):
        ''' naut_pset_05_strategy

        # NEXT, add:
        evaluation.GetStrategies().get_evolved_strategy_func
            ...with inputs...

            see progress there

        # looking to evolve a 2nd simple strategy, where the simple config
        from naut_pset_04_strategy is updated, so that integers can be plugged
        in - as shown by the X, XX, Y, YY below, etc

        # def get_config_strategy(self):
        #     config = EMACrossConfig(
        #         instrument_id=str(self.instrument.id),
        #         bar_type=self.bar_type,
        #         trade_size=Decimal(X),
        #         fast_ema_period=Y,
        #         slow_ema_period=yy,
        #         )
        #     return config
        '''

        # ADF1 pset ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        self.adfset1 = gp.PrimitiveSetTyped("ADF1", [LittleInt], LittleInt, "ARG")

        # boolean operators
        self.adfset1.addPrimitive(operator.and_, [bool, bool], bool)
        self.adfset1.addPrimitive(operator.or_, [bool, bool], bool)
        self.adfset1.addPrimitive(operator.not_, [bool], bool)

        # floating point operators
        # Define a protected division function
        def protectedDiv(left, right):
            try: return left / right
            except ZeroDivisionError: return 1

        self.adfset1.addPrimitive(operator.add, [float,float], float)
        self.adfset1.addPrimitive(operator.sub, [float,float], float)
        self.adfset1.addPrimitive(operator.mul, [float,float], float)
        self.adfset1.addPrimitive(protectedDiv, [float,float], float)

        # logic operators
        # Define a new if-then-else function
        def if_then_else(input, output1, output2):
            if input: return output1
            else: return output2

        self.adfset1.addPrimitive(operator.lt, [float, float], bool)
        self.adfset1.addPrimitive(operator.eq, [float, float], bool)
        self.adfset1.addPrimitive(if_then_else, [bool, float, float], float)

        # terminals
        # self.adfset1.addEphemeralConstant("rand100", partial(random.uniform, 0, 100), float)
        self.adfset1.addTerminal(False, bool)
        self.adfset1.addTerminal(True, bool)

        # ADF0 pset ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        self.adfset0 = gp.PrimitiveSetTyped("ADF0", [LittleInt], LittleInt, "ARG")
        self.adfset0.addPrimitive(operator.add, [LittleInt, LittleInt], LittleInt)
        self.adfset0.addPrimitive(operator.sub, [LittleInt, LittleInt], LittleInt)
        self.adfset0.addPrimitive(operator.mul, [LittleInt], LittleInt)
        # self.adfset0.addPrimitive(protectedDiv, [LittleInt, LittleInt], LittleInt)
        self.adfset0.addPrimitive(operator.neg, [LittleInt], LittleInt)

        # MAIN pset ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        bar_type = "AUD/USD.SIM-1-MINUTE-MID-INTERNAL"
        bar_type2 = "AUD/USD.SIM-1-MINUTE-MID-INTERNAL"
        self.SIM = Venue("SIM")
        inst = TestInstrumentProvider.default_fx_ccy("AUD/USD", self.SIM)
        inst2 = TestInstrumentProvider.default_fx_ccy("AUD/USD",self.SIM)


        # # a first basic primitive set for strongly typed GP using Nautilus
        self.pset = gp.PrimitiveSetTyped("CGPNAUT05",
                                         [], GpRunStrategyInject, "ARG")

        # primary primitive, to enable function
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        # add GpRunStrategyInject as a PRIMITIVE
        self.pset.addPrimitive(GpRunStrategyInject, [GpRunStrategyBaseConfig, str], GpRunStrategyInject)

        # attempt to add GetStrategies with method as primitive...
        self.pset.addPrimitive(GetStrategies.get_config_strategy_no_full_declaration, [], Strategy)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        # HERE HERE

        # looking to implement with: GetStrategies().get_evolved_strategy_func()
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        trade_size = Decimal(1_000_000)
        fast_ema_period = BigInt()
        slow_ema_period = LittleInt()

        self.pset.addPrimitive(GetStrategies.get_evolved_strategy, [], Strategy)

        # need to add the class type, not classes specifically here
        self.pset.addPrimitive(GetStrategies.get_evolved_strategy_1,
                               [CurrencyPair,
                                StrBarType1, Decimal, BigInt, LittleInt],
                               Strategy)

        # using specified int and str classes to reduce degress of freedom:
        self.pset.addPrimitive(BigInt, [BigInt], BigInt)
        self.pset.addPrimitive(LittleInt, [LittleInt], LittleInt)
        self.pset.addPrimitive(str, [StrInstr], StrInstr)
        self.pset.addPrimitive(str, [StrBar], StrBar)

        # pset terminals:
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

        # ADDED PRIMITIVES:
        self.pset.addPrimitive(Decimal, [Decimal], Decimal)
        self.pset.addPrimitive(str, [str], str)
        self.pset.addPrimitive(int, [int], int)
        self.pset.addPrimitive(GpRunStrategyBaseConfig,
                               [StrInstr, StrBar, Decimal, LittleInt, BigInt],
                               GpRunStrategyBaseConfig)
        # ADDED TERMINALS:
        self.pset.addTerminal(Decimal(1_000_000), Decimal)
        self.pset.addTerminal('GpRunStrategyBaseConfig', GpRunStrategyBaseConfig)
        self.pset.addTerminal('GpRunStrategyInject', GpRunStrategyInject)

        # add ADF:
        self.pset.addADF(self.adfset0)
        self.pset.addADF(self.adfset1) # added adfset1, didn't throw errors immediately on addition


        # specify psets, inc adfsets:
        self.psets = (self.pset, self.adfset0) #, self.adfset1)

        return self.psets


    def get_naut_pset_04_strategy(self):
        ''' naut_pset_04_strategy

        # NEXT, add:
        GetStrategies().get_config_strategy_without_full_declaration()

        # looking to evolve a first simple strategy:

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

        # ADF1 pset ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        self.adfset1 = gp.PrimitiveSetTyped("ADF1", [LittleInt], LittleInt, "ARG")

                # boolean operators
        self.adfset1.addPrimitive(operator.and_, [bool, bool], bool)
        self.adfset1.addPrimitive(operator.or_, [bool, bool], bool)
        self.adfset1.addPrimitive(operator.not_, [bool], bool)

        # floating point operators
        # Define a protected division function
        def protectedDiv(left, right):
            try: return left / right
            except ZeroDivisionError: return 1

        self.adfset1.addPrimitive(operator.add, [float,float], float)
        self.adfset1.addPrimitive(operator.sub, [float,float], float)
        self.adfset1.addPrimitive(operator.mul, [float,float], float)
        self.adfset1.addPrimitive(protectedDiv, [float,float], float)

        # logic operators
        # Define a new if-then-else function
        def if_then_else(input, output1, output2):
            if input: return output1
            else: return output2

        self.adfset1.addPrimitive(operator.lt, [float, float], bool)
        self.adfset1.addPrimitive(operator.eq, [float, float], bool)
        self.adfset1.addPrimitive(if_then_else, [bool, float, float], float)

        # terminals
        # self.adfset1.addEphemeralConstant("rand100", partial(random.uniform, 0, 100), float)
        self.adfset1.addTerminal(False, bool)
        self.adfset1.addTerminal(True, bool)

        # ADF0 pset ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        self.adfset0 = gp.PrimitiveSetTyped("ADF0", [LittleInt], LittleInt, "ARG")
        self.adfset0.addPrimitive(operator.add, [LittleInt, LittleInt], LittleInt)
        self.adfset0.addPrimitive(operator.sub, [LittleInt, LittleInt], LittleInt)
        self.adfset0.addPrimitive(operator.mul, [LittleInt], LittleInt)
        # self.adfset0.addPrimitive(protectedDiv, [LittleInt, LittleInt], LittleInt)
        self.adfset0.addPrimitive(operator.neg, [LittleInt], LittleInt)

        # self.adfset0.addADF(adfset2)
        # self.adfset0.renameArguments(ARG0='x0')

        # MAIN pset ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        bar_type = "AUD/USD.SIM-1-MINUTE-MID-INTERNAL"
        bar_type2 = "AUD/USD.SIM-1-MINUTE-MID-INTERNAL"
        self.SIM = Venue("SIM")
        inst = TestInstrumentProvider.default_fx_ccy("AUD/USD", self.SIM)
        inst2 = TestInstrumentProvider.default_fx_ccy("AUD/USD",self.SIM)

        # # a first basic primitive set for strongly typed GP using Nautilus
        self.pset = gp.PrimitiveSetTyped("CGPNAUT04",
                                         [], GpRunStrategyInject, "ARG")

        # primary primitive, to enable function
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        # add GpRunStrategyInject as a PRIMITIVE
        self.pset.addPrimitive(GpRunStrategyInject, [GpRunStrategyBaseConfig, str], GpRunStrategyInject)

        self.pset.addPrimitive(GetStrategies.get_config_strategy_no_full_declaration, [], Strategy)
        # GetStrategies().get_config_strategy_without_full_declaration()
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

        # using specified int and str classes to reduce degress of freedom:
        self.pset.addPrimitive(BigInt, [BigInt], BigInt)
        self.pset.addPrimitive(LittleInt, [LittleInt], LittleInt)
        self.pset.addPrimitive(str, [StrInstr], StrInstr)
        self.pset.addPrimitive(str, [StrBar], StrBar)

        # pset terminals:
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

        # ADDED PRIMITIVES:
        self.pset.addPrimitive(Decimal, [Decimal], Decimal)
        self.pset.addPrimitive(str, [str], str)
        self.pset.addPrimitive(int, [int], int)
        self.pset.addPrimitive(GpRunStrategyBaseConfig,
                               [StrInstr, StrBar, Decimal, LittleInt, BigInt],
                               GpRunStrategyBaseConfig)
        # ADDED TERMINALS:
        self.pset.addTerminal(Decimal(1_000_000), Decimal)
        self.pset.addTerminal('GpRunStrategyBaseConfig', GpRunStrategyBaseConfig)
        self.pset.addTerminal('GpRunStrategyInject', GpRunStrategyInject)

        # add ADF:
        self.pset.addADF(self.adfset0)

        # specify psets, inc adfsets:
        self.psets = (self.pset, self.adfset0)

        return self.psets

    def get_naut_pset_03_strategy(self):
        ''' naut_pset_03_strategy

        # NEXT, add:
        GetStrategies().get_config_strategy_without_full_declaration

        # looking to evolve a first simple strategy:

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

        # ADF1 pset ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        self.adfset1 = gp.PrimitiveSetTyped("ADF1", [LittleInt], LittleInt, "ARG")

                # boolean operators
        self.adfset1.addPrimitive(operator.and_, [bool, bool], bool)
        self.adfset1.addPrimitive(operator.or_, [bool, bool], bool)
        self.adfset1.addPrimitive(operator.not_, [bool], bool)

        # floating point operators
        # Define a protected division function
        def protectedDiv(left, right):
            try: return left / right
            except ZeroDivisionError: return 1

        self.adfset1.addPrimitive(operator.add, [float,float], float)
        self.adfset1.addPrimitive(operator.sub, [float,float], float)
        self.adfset1.addPrimitive(operator.mul, [float,float], float)
        self.adfset1.addPrimitive(protectedDiv, [float,float], float)

        # logic operators
        # Define a new if-then-else function
        def if_then_else(input, output1, output2):
            if input: return output1
            else: return output2

        self.adfset1.addPrimitive(operator.lt, [float, float], bool)
        self.adfset1.addPrimitive(operator.eq, [float, float], bool)
        self.adfset1.addPrimitive(if_then_else, [bool, float, float], float)

        # terminals
        # self.adfset1.addEphemeralConstant("rand100", partial(random.uniform, 0, 100), float)
        self.adfset1.addTerminal(False, bool)
        self.adfset1.addTerminal(True, bool)

        # ADF0 pset ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        self.adfset0 = gp.PrimitiveSetTyped("ADF0", [LittleInt], LittleInt, "ARG")
        self.adfset0.addPrimitive(operator.add, [LittleInt, LittleInt], LittleInt)
        self.adfset0.addPrimitive(operator.sub, [LittleInt, LittleInt], LittleInt)
        self.adfset0.addPrimitive(operator.mul, [LittleInt], LittleInt)
        # self.adfset0.addPrimitive(protectedDiv, [LittleInt, LittleInt], LittleInt)
        self.adfset0.addPrimitive(operator.neg, [LittleInt], LittleInt)

        # self.adfset0.addADF(adfset2)
        # self.adfset0.renameArguments(ARG0='x0')

        # MAIN pset ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        bar_type = "AUD/USD.SIM-1-MINUTE-MID-INTERNAL"
        bar_type2 = "AUD/USD.SIM-1-MINUTE-MID-INTERNAL"
        self.SIM = Venue("SIM")
        inst = TestInstrumentProvider.default_fx_ccy("AUD/USD", self.SIM)
        inst2 = TestInstrumentProvider.default_fx_ccy("AUD/USD",self.SIM)

        # # a first basic primitive set for strongly typed GP using Nautilus
        self.pset = gp.PrimitiveSetTyped("CGPNAUT03",
                                         [], GpRunStrategyInject, "ARG")
        # primary primitive, to enable function
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        self.pset.addPrimitive(GpRunStrategyInject, [GpRunStrategyBaseConfig, str], GpRunStrategyInject)
        # add GpRunStrategyInject as a PRIMITIVE

        # using specified int and str classes to reduce degress of freedom:
        self.pset.addPrimitive(BigInt, [BigInt], BigInt)
        self.pset.addPrimitive(LittleInt, [LittleInt], LittleInt)
        self.pset.addPrimitive(str, [StrInstr], StrInstr)
        self.pset.addPrimitive(str, [StrBar], StrBar)

        # pset terminals:
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

        # ADDED PRIMITIVES:
        self.pset.addPrimitive(Decimal, [Decimal], Decimal)
        self.pset.addPrimitive(str, [str], str)
        self.pset.addPrimitive(int, [int], int)
        self.pset.addPrimitive(GpRunStrategyBaseConfig,
                               [StrInstr, StrBar, Decimal, LittleInt, BigInt],
                               GpRunStrategyBaseConfig)
        # ADDED TERMINALS:
        self.pset.addTerminal(Decimal(1_000_000), Decimal)
        self.pset.addTerminal('GpRunStrategyBaseConfig', GpRunStrategyBaseConfig)
        self.pset.addTerminal('GpRunStrategyInject', GpRunStrategyInject)

        # add ADF:
        self.pset.addADF(self.adfset0)

        # specify psets, inc adfsets:
        self.psets = (self.pset, self.adfset0)

        return self.psets

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
        self.adfset0.addPrimitive(operator.mul, [LittleInt, LittleInt], LittleInt)
        # self.adfset0.addPrimitive(protectedDiv, [LittleInt, LittleInt], LittleInt)
        self.adfset0.addPrimitive(operator.neg, [LittleInt], LittleInt)

        # self.adfset0.addADF(adfset2)
        # self.adfset0.renameArguments(ARG0='x0')

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

    def __len__(self):
        return 1

class StrBar(str):
    def pass_method(self):
        pass

    def __len__(self):
        return 1

class StrBarType1(str):
    ''' Sets bar type to X, as a class variable for evolution'''
    def __init__(self):
        return "AUD/USD.SIM-1-MINUTE-MID-INTERNAL"

    def pass_method(self):
        pass

    def __len__(self):
        return 1

class BigInt(int):
    def pass_method(self):
        pass

    def __len__(self):
        return 1

class LittleInt(int):
    def pass_method(self):
        pass

if __name__ == '__main__':
    pass

    # uncomment the below and run to have a look into a pset created above:

    a = 'naut_pset_03_strategy'
    b = 'test_pset5a'
    c = 'test_adf_symbreg_pset'
    d = 'naut_pset_04_strategy'
    e = 'naut_pset_05_strategy'
    gpp = GpPsets()
    pset_and_adf = gpp.get_named_pset(e)
    print(pset_and_adf)
    print(f"{type(pset_and_adf[0])} named: {pset_and_adf[0].name}")

    # SIM = Venue("SIM")
    # inst2 = TestInstrumentProvider.default_fx_ccy("AUD/USD",SIM)
    # print(type(inst2))

    # print(f"{type(pset_and_adf[1])} named: {pset_and_adf[1].name}")
    # # print('looking at terminals:')
    # print('count of terminals: ', one.terms_count,
    #       ' ... n.b. always one more than actual, due to base class')
    # term_keys = list(one.terminals.keys())
    # print(term_keys)
    # list_terminals = one.terminals.get(term_keys[0])
    # print(list_terminals)
    # prim_names = list(one.context.keys())
    # print(prim_names)
