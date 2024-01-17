import numpy
import random
import logging
import traceback

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

from condorgp.interfaces.gp_provider import GpProvider

class GpDeap(GpProvider):
    def __init__(self):
        '''
            Provides the workings for Deap to operate.
        '''
        self.verbose = 0

    def set_defined_pset(self, pset_obj,
                 new_pset_name = '',
                 functions: dict = '',
                 terminals: dict = ''):
        ''' sets the population set for the gp run.
        inputs: the functions and terminals by name, their arrity and function
        '''

        if new_pset_name:
            try:
                logging.debug(f"Gp_Deap SETTING pset: {new_pset_name}")
                self.pset = pset_obj.get_named_pset(new_pset_name)
            except Exception as e:
                logging.warn("Gp_Deap WARNING, default untyped used instead: " + str(e))
                self.pset = pset_obj.get_default_untyped()

        return self.pset


    def set_gp_params(self, params: dict):
        '''
        Set the major parameters for genetic programming with Deap.

        Fitness function, Individual and GP tree base classes. Population,
        genetic operators, initiation of population mechanism.
        '''
        try:
            # fundamentals for the gp tree
            creator.create("FitnessMax", base.Fitness, weights=(1.0,))
            creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

            # toobox and it's components, including population
            self.toolbox = base.Toolbox()
            self.toolbox.register("expr",
                                gp.genHalfAndHalf,
                                pset=self.pset,
                                min_=1,
                                max_=2)
            self.toolbox.register("individual",
                                tools.initIterate,
                                creator.Individual,
                                self.toolbox.expr)
            self.toolbox.register("population",
                                tools.initRepeat,
                                list,
                                self.toolbox.individual)
            self.toolbox.register("compile", gp.compile, pset=self.pset)

            self.rand = random.seed(318)

            self.toolbox.register("select", tools.selTournament, tournsize=3)
            self.toolbox.register("mate", gp.cxOnePoint)
            self.toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
            self.toolbox.register('mutate',
                                gp.mutUniform,
                                expr=self.toolbox.expr_mut,
                                pset=self.pset)
        except BaseException as e:
            tb = ''.join(traceback.format_tb(e.__traceback__))
            logging.debug(f"gp_deap.set_gp_params ERROR: \n {tb}")


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

    def set_pop_size(self, pop_size: int = 2):
        ''' Sets population size as required '''
        self.pop_size = pop_size
        self.pop = self.toolbox.population(n=self.pop_size)

    def set_evaluator(self, new_evaluator):
        ''' Sets evaluation function '''
        self.toolbox.register("evaluate", new_evaluator)

    def set_gens(self, no_gens: int = 2):
        ''' Sets no generations as required '''
        self.ngen = no_gens

    def set_stats(self, stat_params: dict):
        ''' Set the statistics used for the gp run '''
        self.hof = tools.HallOfFame(5)
        self.stats = tools.Statistics(lambda ind: ind.fitness.values)
        self.stats.register("avg", numpy.mean)
        self.stats.register("std", numpy.std)
        self.stats.register("min", numpy.min)
        self.stats.register("max", numpy.max)

        self.logbook = tools.Logbook()
        self.logbook.header = "gen", "evals", "std", "min", "avg", "max"

    def run_gp(self):
        ''' Do a GP run, using DEAP algorithms.eaSimple '''
        inputs = [0,0,0]
        self.values = inputs

        self.pop, self.logbook = algorithms.eaSimple(self.pop,
                                                    self.toolbox,
                                                    0.5,
                                                    0.1,
                                                    self.ngen,
                                                    self.stats,
                                                    halloffame=self.hof)
        return self.pop, self.stats, self.hof, self.logbook
