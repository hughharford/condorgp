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
            logging.info(f"GpDeapADF SETTING pset: {new_pset_name}")
            self.psets = gp_psets_cls.get_named_pset(new_pset_name)

        if not self.psets:
            logging.warn(f"GpDeapADF: running pset "+
                         "{self.pset.__name__}")
            self.psets = gp_psets_cls.get_naut_pset_01()

        if not self.psets:
            logging.warn(f"ERROR GpDeapADF: no pset!")

        logging.debug(self.psets[0].name)
        logging.debug(self.psets[1].name)

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
        self.rand = random.seed(318)

        # fundamentals for the gp tree
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Tree", gp.PrimitiveTree)

        creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

        self.toolbox = base.Toolbox()
        self.toolbox.register('adf_expr0', gp.genFull, pset=self.adfset, min_=1, max_=2)
        self.toolbox.register("main_expr", gp.genHalfAndHalf, pset=self.pset, min_=1, max_=2)

        self.toolbox.register('ADF0', tools.initIterate, creator.Tree, self.toolbox.adf_expr0)
        self.toolbox.register('MAIN', tools.initIterate, creator.Tree, self.toolbox.main_expr)

        self.func_cycle = [self.toolbox.MAIN, self.toolbox.ADF0]

        self.toolbox.register("individual", tools.initCycle, creator.Individual, self.func_cycle)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

        self.toolbox.register('compile', gp.compileADF, psets=self.psets)
        # evaluate set elsewhere
        self.toolbox.register("select", tools.selTournament, tournsize=3)
        self.toolbox.register("mate", gp.cxOnePoint)
        self.toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
        self.toolbox.register('mutate', gp.mutUniform, expr=self.toolbox.expr_mut)
