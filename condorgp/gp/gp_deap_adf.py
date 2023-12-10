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


        # if functions == '' and terminals == '':
        #     return self.pset
        # else:
        #     print("need to do something to add primitives")
            # self.pset.addPrimitive(
            #     functions['method'], functions['arrity'], functions['name'])

        return self.pset


    def set_gp_params(self, params: dict):
        '''
        Set the major parameters for genetic programming with Deap.

        Fitness function, Individual and GP tree base classes. Population,
        genetic operators, initiation of population mechanism.
        '''

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
