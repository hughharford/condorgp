#    This file is a copied example file from EAP.
#
#
#    EAP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    EAP is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with EAP. If not, see <http://www.gnu.org/licenses/>.

from distutils.cygwinccompiler import CygwinCCompiler
from logging import NOTSET
import operator
import math
import random
import itertools

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

from condorgp.util.log import CondorLogger
from condorgp.factories.factory import Factory

class CondorDeapLearning:
    def __init__(self):
        '''
            Setup the gp run
        '''

        # logging
        logger = CondorLogger()
        self.log = logger.get_logger()
        filler_INIT = '>'*10
        self.log.info(f"{filler_INIT}, {__class__} - DEAP gp - run began {filler_INIT}")

        self.util = Factory().get_utils()

        # first primitive set:
        self.pset = gp.PrimitiveSet("INITIAL", 4)
        # can add own defined function, with 4 inputs
        # just can't yet control where it comes
        self.pset.addPrimitive(baseSplit4, 4, name="baseSplit4")
        self.pset.addPrimitive(numpy.add, 2, name="vadd")
        self.pset.addPrimitive(numpy.subtract, 2, name="vsub")
        self.pset.addPrimitive(numpy.multiply, 2, name="vmul")
        self.pset.addPrimitive(protectedDiv, 2)
        self.pset.addPrimitive(numpy.negative, 1, name="vneg")
        self.pset.addPrimitive(numpy.cos, 1, name="vcos")
        self.pset.addPrimitive(numpy.sin, 1, name="vsin")
        self.pset.addEphemeralConstant("rand101", lambda: random.randint(-1,1))
        self.pset.addEphemeralConstant("rand202", lambda: random.randint(-2,2))
        self.pset.renameArguments(ARG0='x')

        # fundamentals for the gp tree
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

        # toobox and it's components, including population
        self.toolbox = base.Toolbox()
        self.toolbox.register("expr", gp.genHalfAndHalf, pset=self.pset, min_=1, max_=2)
        self.toolbox.register("individual",
                              tools.initIterate,
                              creator.Individual,
                              self.toolbox.expr)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        self.toolbox.register("compile", gp.compile, pset=self.pset)

        self.samples = numpy.linspace(-1, 1, 10000)
        self.values = self.samples**4 \
                            + self.samples**3 \
                            + self.samples**2 \
                            + self.samples

        self.rand = random.seed(318)

        self.pop = self.toolbox.population(n=300)
        self.hof = tools.HallOfFame(5)
        self.stats = tools.Statistics(lambda ind: ind.fitness.values)
        self.stats.register("avg", numpy.mean)
        self.stats.register("std", numpy.std)
        self.stats.register("min", numpy.min)
        self.stats.register("max", numpy.max)

        # toolbox.register("evaluate", evalSymbReg)
        self.toolbox.register("evaluate", self.evalIntoAndFromLean)
        self.toolbox.register("select", tools.selTournament, tournsize=3)
        self.toolbox.register("mate", gp.cxOnePoint)
        self.toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
        self.toolbox.register('mutate', gp.mutUniform, expr=self.toolbox.expr_mut, pset=self.pset)

    def evalSymbReg(self, individual):
        # Transform the tree expression in a callable function
        func = self.toolbox.compile(expr=individual)
        # Evaluate the sum of squared difference between the expression


        # and the real function values : x**4 + x**3 + x**2 + x
        diff = numpy.sum((func(self.samples) - self.values)**2)
        return diff

    def evalIntoAndFromLean(self, individual):
        # Transform the tree expression in a callable function
        func = self.toolbox.compile(expr=individual)
        # output a compile function to a file, so it can be run via Lean
        # TO DO:

        # get fitness from the Lean log
        Return_over_MDD = 'STATISTICS:: Return Over Maximum Drawdown'
        got = self.util.get_key_line_in_lim(Return_over_MDD)
        new_fitness = float(self.util.get_last_chars(got[0]))

        fill = '>'*17 + '_'*7
        # print(f'new fitness {fill}{new_fitness}')
        # returns a float in a tuple, i.e.
        #                               .68704775238,
        return new_fitness,


    def main(self):
        # set to 1 generation for testing
        self.pop, self.logbook = algorithms.eaSimple(self.pop, self.toolbox, 0.5, 0.1, 1, self.stats, halloffame=self.hof)

        return self.pop, self.stats, self.hof, self.logbook

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

def baseSplit4(in1, in2, in3, in4):
    return 0

if __name__ == "__main__":
    # run gp, outputting population, stats, hall of fame:
    ccc = CondorDeapLearning()
#    ccc.run()

    # SAMPLE RUN
    ccc.main()

    print('ccc.logbook in full:')
    print(ccc.logbook)

    print('gen')
    gen = ccc.logbook.select("gen")
    print(gen)

    print('gen, avg')
    gen, avg = ccc.logbook.select("gen", "max")
    print(gen, avg)

    print()
    print("max fitness found: " + str(ccc.logbook.select("max")[-1]))

    print()
    print('print of each individual might give code enough:\n')
    for ind in ccc.pop:
        print(ind)
        print('****************')

    # *******************************************************************
    learning = 1
    if learning == 1:
        # see what we got:
        ccc.log.info('Hall of fame:')
        for x, individual in enumerate(ccc.hof):
            ccc.log.info(ccc.hof.items[x])

        ccc.log.info(f'primitives_count = {ccc.pset.prims_count}')
        ccc.log.info(f'terminals_count = {ccc.pset.terms_count}')
        print("NOTE: count of terminals includes base terminal class => -1")

        # TRYING TO ACCESS PRIMITIVE SET
        # ccc.log.info(ccc.pset.primitives.items[0])
        # print(ccc.toolbox.__dict__)

        print()

        print('see the first Primitive in 1st individual')
        print(ccc.toolbox.select(ccc.pop, 1)[0])

        print('all the individuals')
        selection = ccc.toolbox.select(ccc.pop, len(ccc.pop))
        for x in range(len(selection)):
            print(selection[x])

        # see the pset as a list
        print('pset.__dict__:')
        print(list(ccc.pset.__dict__))

        print()

        # print the whole pset
        # print((ccc.pset.__dict__))

        print()

        # terminals is a defaultdict
        print('pset.terminals:')
        print((ccc.pset.terminals))

        print()

        print('the context keys holds the names of the func & terminal set')
        context_list = list(ccc.pset.context.keys())
        print(f'{context_list} and length: {len(context_list)-1}')

        print('this shows the user added function is <class "numpy.ufunc">')
        print(type(ccc.pset.context.get(context_list[1])))

        # name of the primitive set
        print('pset.name: ')
        print(ccc.pset.name)

        print()

        print('looking at count of primitives or terminals:')
        term_keys = list(ccc.pset.terminals.keys())
        list_terminals = ccc.pset.terminals.get(term_keys[0])
        print(type(list_terminals[2]))

        print()

        print('ccc.stats.__dict__:')
        print(ccc.stats.__dict__)

        print()
