import numpy
import random
import logging
import traceback
import pickle
import os

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

from condorgp.gp.gp_deap_adf_cp import GpDeapAdfCp
from condorgp.util.log import CondorLogger
from condorgp.params import Params

class GpDeapElitist(GpDeapAdfCp):
    def __init__(self):
        '''
            Provides the workings for Deap to operate.
            This class additionally achieves elitism.
            Inherits from GpDeapAdfCp.
        '''
        super.__init__

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

            # elitism update here
            self.toolbox.register("select", tools.selTournament, tournsize=3)
            self.toolbox.register("mate", gp.cxOnePoint)
            self.toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
            self.toolbox.register('mutate',
                                gp.mutUniform,
                                expr=self.toolbox.expr_mut,
                                pset=self.pset)

        except BaseException as e:
            logging.error(f"gp_deap_elitist ERROR in setup {e}")
            tb = ''.join(traceback.format_tb(e.__traceback__))
            logging.debug(f"gp_deap_elitist: {tb}")
