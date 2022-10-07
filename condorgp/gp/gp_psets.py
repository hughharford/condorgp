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
        except:
            print("GpPsets ERROR")
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

    def get_test_psetA(self):
        ''' test pset A '''
        self.testA = gp.PrimitiveSet("test pset A", 0)
        self.testA.addPrimitive(numpy.multiply, 2, name="vmul")
        return self.testA

    def get_test_psetB(self):
        ''' test pset B '''
        self.testB = gp.PrimitiveSet("test pset B", 0)
        self.testB.addPrimitive(numpy.add, 2, name="vadd")
        self.testB.addPrimitive(print, 1, name="print")
        self.testB.addTerminal("***_***_***", "3x3")
        return self.testB

    def get_test_psetC(self):
        ''' test pset C '''
        self.testC = gp.PrimitiveSet("test pset C", 1)
        self.testC.addPrimitive(self.log.info, 1, name="self.log.info")
        self.testC.renameArguments(ARG0='x0')
        return self.testC

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
