import numpy
import random

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

from condorgp.interfaces.gp_provider import GpProvider

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

class GpDependency(GpProvider):
    def __init__(self):
        pass


    def set_pset(self, functions: dict, terminals: dict):
        ''' sets the population set for the gp run.
        inputs: the functions and terminals by name, their arrity and function
        '''
        # primitive set, EXAMPLE from DEAP:
        self.pset = gp.PrimitiveSet("MAIN", 1)
        self.pset.addPrimitive(numpy.add, 2, name="vadd")
        self.pset.addPrimitive(numpy.subtract, 2, name="vsub")
        self.pset.addPrimitive(numpy.multiply, 2, name="vmul")
        self.pset.addPrimitive(
            functions['method'], functions['arrity'], functions['name'])
        self.pset.addPrimitive(numpy.negative, 1, name="vneg")
        self.pset.addPrimitive(numpy.cos, 1, name="vcos")
        self.pset.addPrimitive(numpy.sin, 1, name="vsin")
        self.pset.addEphemeralConstant("rand101", lambda: random.randint(-1,1))
        self.pset.renameArguments(ARG0='x')

    def get_pset(self):
        return self.pset

    def set_gp_params(self, params: dict):

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

        self.rand = random.seed(318)

        # attempting insert of these lines here. have seperated out this line:
        #    toolbox.register("evaluate", evalSymbReg)
        # which normally appears before these 4...
        self.toolbox.register("select", tools.selTournament, tournsize=3)
        self.toolbox.register("mate", gp.cxOnePoint)
        self.toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
        self.toolbox.register('mutate', gp.mutUniform, expr=self.toolbox.expr_mut, pset=self.pset)

    def set_inputs(self, inputs: dict):
        '''
        Set the input values for fitness evaluation:
        '''
        # in this case, just the EXAMPLE polynomial
        self.samples = numpy.linspace(-1, 1, 10000)
        self.values = self.samples**4 \
                            + self.samples**3 \
                            + self.samples**2 \
                            + self.samples

    def set_pop_size(self, pop_size: int):
        '''
        Sets the population as the required
        '''
        self.pop = self.toolbox.population(n=pop_size)

    def set_evaluator(self, new_evaluator):
        '''
        Sets evaluation function
        '''
        self.toolbox.register("evaluate", new_evaluator)

    def set_stats(self, stat_params: dict):
        '''
        Set the statistics used for the gp run
        '''
        self.hof = tools.HallOfFame(5)
        self.stats = tools.Statistics(lambda ind: ind.fitness.values)
        self.stats.register("avg", numpy.mean)
        self.stats.register("std", numpy.std)
        self.stats.register("min", numpy.min)
        self.stats.register("max", numpy.max)

    def multi_stats(self):
        self.stats_fit = tools.Statistics(key=lambda ind: ind.fitness.values)
        self.stats_size = tools.Statistics(key=len)
        self.mstats = tools.MultiStatistics(fitness=self.stats_fit,
                                            size=self.stats_size)
        self.mstats.register("max", numpy.max)


    def set_gens(self, no_gens: int = 2):
        self.ngen = no_gens

    def run_gp(self):
        '''
        Do a GP run, with default 1 generation for testing
        '''
        self.logbook  = algorithms.eaSimple(self.pop, self.toolbox, 0.5, 0.1, self.ngen, \
                            self.stats, halloffame=self.hof)
        return self.pop, self.stats, self.hof, self.logbook
