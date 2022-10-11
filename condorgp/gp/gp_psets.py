from deap import gp
import numpy
import random
import operator
import math

from condorgp.util.log import CondorLogger

class GpPsets:
    def __init__(self, custom_funcs):
        self.custom_funcs = custom_funcs
        self.log = CondorLogger().get_logger()

    def get_named_pset(self, named_pset):
        try:
            return eval('self.get_' + named_pset + '()')
        except Exception as e:
            print("GpPsets ERROR: " + str(e))
            return None

    def get_default_untyped(self):
         # basic untyped deap.gp.PrimitiveSet:
        self.default_untyped = gp.PrimitiveSet("MAIN", 1)
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
        self.test_base = gp.PrimitiveSet("test_base", 1)
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
        self.test6a = gp.PrimitiveSet("test pset 6a", 1)
        self.test6a.addTerminal(self.get_alpha_model_A, 'model_A')
        self.test6a.renameArguments(ARG0='x0')

        # self.test6a.addTerminal(self.get_alpha_model_B, name='model_B')
        # self.test6a.addTerminal(self.get_alpha_model_C, name='model_C')
        # self.test6a.addTerminal(self.get_alpha_model_D, name='model_D')
        return self.test6a

    def get_test_pset6b(self):
        ''' test pset 6b '''
        self.test6b = gp.PrimitiveSet("test pset 6b", 1)
        self.test6b.addTerminal(self.get_alpha_model_A, 'model_A')
        self.test6b.renameArguments(ARG0='x0')

        # self.test6b.addTerminal(self.get_alpha_model_B, name='model_B')
        # self.test6b.addTerminal(self.get_alpha_model_C, name='model_C')
        # self.test6b.addTerminal(self.get_alpha_model_D, name='model_D')
        return self.test6b

    def get_extant_line(self):
        extant_line = '''
    def newly_injected_code(self):
        return ConstantAlphaModel(InsightType.Price,
                                  InsightDirection.Up,
                                  timedelta(minutes = 20),
                                  0.025, None
                                  )'''
        return extant_line

    def get_alpha_model_A(self, input):
        line = '''
    def newly_injected_code(self):
        return HistoricalReturnsAlphaModel()'''
        return line

    def get_alpha_model_B(self, input):
        line = '''
    def newly_injected_code(self):
        return EmaCrossAlphaModel()'''
        return line

    def get_alpha_model_C(self):
        line = '''
    def newly_injected_code(self):
        return MacdAlphaModel()'''
        return line

    def get_alpha_model_D(self):
        line = '''
    def newly_injected_code(self):
        return RsiAlphaModel()'''
        return line

    def get_adf2(self):
        self.adfset2 = gp.PrimitiveSet("ADF2", 2)
        self.adfset2.addPrimitive(operator.add, 2)
        self.adfset2.addPrimitive(operator.sub, 2)
        self.adfset2.addPrimitive(operator.mul, 2)
        self.adfset2.addPrimitive(self.custom_funcs.protectedDiv, 2)
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
        self.adfset1.addPrimitive(self.custom_funcs.protectedDiv, 2)
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
        self.adfset0.addPrimitive(self.custom_funcs.protectedDiv, 2)
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
    print('Pset name = ', one.name)
    one.addPrimitive(operator.add, 2, name="NEW ONE, NEW ONE")
    print(one.terminals)

    print('looking at terminals:')
    print('count of terminals: ', one.terms_count,
          ' ... n.b. always one more than actual, due to base class')
    term_keys = list(one.terminals.keys())
    print(term_keys)
    list_terminals = one.terminals.get(term_keys[0])
    print(list_terminals)

    prim_names = list(one.context.keys())
    print(prim_names)
