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

from condorgp.gp.gp_deap_adf import GpDeapADF

from condorgp.util.log import CondorLogger
from condorgp.params import Params

class GpDeapElitist(GpDeapADF):
    def __init__(self):
        '''
            Provides the workings for Deap to operate.
            This class additionally achives elitism.
            Inherits from GpDeapAdf.
        '''
        super().__init__()
        self.p = Params()

    def set_gp_params(self, params: dict):
        '''
        Now to handle ADFs
        Set the major parameters for genetic programming with Deap.

        Fitness function, Individual and GP tree base classes. Population,
        genetic operators, initiation of population mechanism.
        '''
        logging.debug(f"gp_deap_elitist.set_gp_params")
        logging.debug(f"self.adfset name: {self.adfset.name}")
        logging.debug(f"self.pset name: {self.pset.name}")

        try:

            # fundamentals for the gp tree
            creator.create("FitnessMax", base.Fitness, weights=(1.0,))
            creator.create("Tree", gp.PrimitiveTree)

            creator.create("Individual", list, fitness=creator.FitnessMax) # list was gp.PrimitiveTree

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

            # changes here for 'select'
            # self.toolbox.register("select", tools.selTournament, tournsize=3)
            self.toolbox.register("select",
                                  self.selElitistAndTournament,
                                  no_elite=self.p.naut_dict['ELITE_NO'],
                                  tournsize=3)

            self.toolbox.register("mate", gp.cxOnePoint)
            self.toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
            self.toolbox.register('mutate', gp.mutUniform, expr=self.toolbox.expr_mut)

            self.ind = self.toolbox.individual()

        except BaseException as e:
            tb = ''.join(traceback.format_tb(e.__traceback__))
            logging.debug(f"gp_deap.set_gp_params ERROR: \n {tb}")

    def selElitistAndTournament(self,
                                individuals,
                                k,
                                no_elite,
                                tournsize):
        '''
        deap_users suggestion:
        https://groups.google.com/g/deap-users/c/iannnLI2ncE/m/eI4BcVcwFwMJ

        '''
        # selBest would be the obvious choice, but this assumes FitnessMin setup
        # therefore, selWorst to choose those individuals with highest fitness
        best = tools.selWorst(individuals,
                             int(no_elite))

        tournament = tools.selTournament(individuals,
                                         int(k-no_elite),
                                         tournsize=tournsize)
        return best + tournament
