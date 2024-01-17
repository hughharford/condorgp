import numpy
import random
import logging

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

from condorgp.gp.gp_deap import GpDeap
from condorgp.util.log import CondorLogger

class GpDeapADF(GpDeap):
    def __init__(self):
        '''
            Provides the workings for Deap to operate.
            This class additionally achieves ADF usage (custom algorithm).
            Inherits from GpDeap. 
        '''
        super.__init__

    def set_defined_pset(self, gp_psets_cls,
                 new_pset_name = '',
                 functions: dict = '',
                 terminals: dict = ''):
        ''' sets the population set for the gp run.
        inputs: the functions and terminals by name, their arrity and function
        '''

        if new_pset_name:
            logging.debug(f"GpDeapADF SETTING pset: {new_pset_name}")
            self.psets = gp_psets_cls.get_named_pset(new_pset_name)

        # if not self.psets:
        #     logging.warning(f"GpDeapADF: running pset "+
        #                  "{self.pset.__name__}")
        #     # self.psets = gp_psets_cls.get_naut_pset_01()

        if not self.psets:
            logging.warning(f"ERROR GpDeapADF: no pset!")

        # # seperate out main and adf:
        self.pset = self.psets[0]
        self.adfset = self.psets[1]

        return self.psets


    def set_gp_params(self, params: dict):
        '''
        Now to handle ADFs
        Set the major parameters for genetic programming with Deap.

        Fitness function, Individual and GP tree base classes. Population,
        genetic operators, initiation of population mechanism.
        '''
        # self.rand = random.seed(318) - now sets in run_gp

        logging.debug(f"self.adfset name: {self.adfset.name}")
        logging.debug(f"self.pset name: {self.pset.name}")

        # fundamentals for the gp tree
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Tree", gp.PrimitiveTree)

        creator.create("Individual", list, fitness=creator.FitnessMax) # list was gp.PrimitiveTree

        # NO DICE __ Adding these reduced __init__ completion
        # creator.create("ADF0", gp.PrimitiveTree, pset=self.adfset)
        # creator.create("MAIN", gp.PrimitiveTree, pset=self.pset)

        self.toolbox = base.Toolbox()
        self.toolbox.register('adf_expr0', gp.genFull, pset=self.adfset, min_=1, max_=2)
        self.toolbox.register("main_expr", gp.genHalfAndHalf, pset=self.pset, min_=1, max_=2)

        self.toolbox.register('ADF0', tools.initIterate, creator.Tree, self.toolbox.adf_expr0)
        self.toolbox.register('MAIN', tools.initIterate, creator.Tree, self.toolbox.main_expr)

        # NO DICE __ Adding these reduced __init__ completion
        # self.toolbox.register('ADF1', tools.initIterate, creator.ADF0, self.toolbox.adf_expr0)
        # self.toolbox.register('MAIN', tools.initIterate, creator.MAIN, self.toolbox.main_expr)

        self.func_cycle = [self.toolbox.MAIN, self.toolbox.ADF0]

        self.toolbox.register("individual", tools.initCycle, creator.Individual, self.func_cycle)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

        self.toolbox.register('compile', gp.compileADF, psets=self.psets)
        # evaluate set elsewhere
        self.toolbox.register("select", tools.selTournament, tournsize=3)
        self.toolbox.register("mate", gp.cxOnePoint)
        self.toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
        self.toolbox.register('mutate', gp.mutUniform, expr=self.toolbox.expr_mut)

        self.ind = self.toolbox.individual()

    def run_gp(self, inputs):
        ''' GpDeapADF. Do a GP run.
            previously used DEAP algorithms.eaSimple but this won't handle ADFs
            so trying example for '''

        logging.debug(f"gp_deap_adf.run_gp: {'@'*5}")

        random.seed(3227)
        NGEN = self.ngen
        NPOP = self.pop_size
        CXPB, MUTPB = 0.5, 0.2

        try:
            pop = self.toolbox.population(n=NPOP)
            # Evaluate the entire population
            for ind in pop:
                ind.fitness.values = self.toolbox.evaluate(ind)

        except BaseException as e:
            logging.error(f"gp_deap_adf.run_gp ERROR: {e}")

        self.hof.update(pop)
        self.record = self.stats.compile(pop)
        self.logbook.record(gen=0, evals=len(pop), **self.record)
        if self.verbose:
            logging.info(self.logbook.stream)

        for g in range(1, NGEN):
            # Select the offspring
            self.offspring = self.toolbox.select(pop, len(pop))
            # Clone the offspring
            self.offspring = [self.toolbox.clone(ind) for ind in self.offspring]

            # Apply crossover and mutation
            for ind1, ind2 in zip(self.offspring[::2], self.offspring[1::2]):
                for tree1, tree2 in zip(ind1, ind2):
                    if random.random() < CXPB:
                        self.toolbox.mate(tree1, tree2)
                        del ind1.fitness.values
                        del ind2.fitness.values

            for ind in self.offspring:
                for tree, pset in zip(ind, self.psets):
                    if random.random() < MUTPB:
                        self.toolbox.mutate(individual=tree, pset=pset)
                        del ind.fitness.values

            # Evaluate the individuals with an invalid fitness
            invalids = [ind for ind in self.offspring if not ind.fitness.valid]
            for ind in invalids:
                ind.fitness.values = self.toolbox.evaluate(ind)

            # Replacement of the population by the offspring
            pop = self.offspring
            self.hof.update(pop)
            self.record = self.stats.compile(pop)
            self.logbook.record(gen=g, evals=len(invalids), **self.record)
            if self.verbose:
                logging.info(self.logbook.stream)

        if self.verbose:
            logging.info('Best individual : ', self.hof[0][0], self.hof[0].fitness)

        return pop, self.stats, self.hof, self.logbook
