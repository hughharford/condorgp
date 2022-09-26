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

from logging import NOTSET
import operator
import math
import random

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

from condorgp.utils import Utils
from condorgp.util.log import CondorLogger

class CondorDeap:
    def __init__(self):
        '''
            Setup the gp run
        '''
        self.util = Utils()

        # logging
        logger = CondorLogger()
        self.log = logger.get_logger()
        filler_INIT = '>'*10
        self.log.info(f"{filler_INIT}, {__class__} - DEAP gp - run began {filler_INIT}")

        # primitive set:
        self.pset = gp.PrimitiveSet("MAIN", 1)
        self.pset.addPrimitive(numpy.add, 2, name="vadd")
        self.pset.addPrimitive(numpy.subtract, 2, name="vsub")
        self.pset.addPrimitive(numpy.multiply, 2, name="vmul")
        self.pset.addPrimitive(protectedDiv, 2)
        self.pset.addPrimitive(numpy.negative, 1, name="vneg")
        self.pset.addPrimitive(numpy.cos, 1, name="vcos")
        self.pset.addPrimitive(numpy.sin, 1, name="vsin")
        self.pset.addEphemeralConstant("rand101", lambda: random.randint(-1,1))
        self.pset.renameArguments(ARG0='x')

        # fundamentals for the gp tree
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

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
        # run lean




        Return_over_MDD = 'STATISTICS:: Return Over Maximum Drawdown'
        new_fitness = self.util.get_keyed_line_within_limits(Return_over_MDD)[0]
        fill = '>'*41
        print(f'new fitness {fill}{new_fitness}')
        # returns a float in a tuple, i.e.
        #                               14736.68704775238,
        return new_fitness,

    def main(self):
        # set to 1 generation for testing
        algorithms.eaSimple(self.pop, self.toolbox, 0.5, 0.1, 1, self.stats, halloffame=self.hof)

        return self.pop, self.stats, self.hof

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

if __name__ == "__main__":
    # run gp, outputting population, stats, hall of fame:
    ccc = CondorDeap()
#    ccc.run()

    # SAMPLE RUN
    pop, stats, hof = ccc.main()
    # see what we got:
    ccc.log.info('Hall of fame:')
    for x, individual in enumerate(hof):
        ccc.log.info(hof.items[x])

class EvaluateWithLean():

    def __init__(ind_path_n_filename):
        print("ind_path_n_filename is: " + ind_path_n_filename)
        pass

    def evaluate_with_lean():
        '''
        Takes the premade class and pushes it to lean/localpackages/condorgp
        Then runs lean
        '''
            #     copy_config_in(input_ind)
        pass #copy_algo_in(input_ind)
