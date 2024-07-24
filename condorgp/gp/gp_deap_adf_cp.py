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
from condorgp.params import Params
from condorgp.util import utils as u

class GpDeapAdfCp(GpDeapADF):
    def __init__(self):
        '''
            Provides the workings for Deap to operate.
            This class additionally achieves checkpointing.
            Inherits from GpDeapADF.
        '''
        super().__init__()
        self.checkpointfile = None
        self.checkpoint_freq = None
        self.checkpointfilepath = None
        self.p = Params()
        self.u = u.Utils()
        self.run_done_txt = self.p.naut_dict['RUN_DONE_TEXT']

    def run_gp(self, inputs=None):
        ''' GpDeapADF. Do a GP run.
            previously used DEAP algorithms.eaSimple but this won't handle ADFs
            so trying example for
        '''
        logging.debug(f"{'&&'*5} gp_deap_adf_cp.run_gp: {'&&'*5}")
        CXPB, MUTPB = 0.5, 0.2
        N_GEN = self.ngen
        N_POP = self.pop_size
        CP_FREQ = self.checkpoint_freq
        logging.debug(f"run_gp: NGEN: {N_GEN} pop_size = {N_POP}")

        try:
            if os.path.isfile(self.checkpointfilepath):
                # A file name has been given, then load the data from the file
                with open(self.checkpointfilepath, "rb") as cp_file:
                    cp = pickle.load(cp_file)
                self.pop = cp["population"]
                start_gen = cp["generation"]
                N_GEN = N_GEN + start_gen # each run increments g_done forward
                self.hof = cp["halloffame"]
                self.logbook = cp["logbook"]
                random.setstate(cp["rndstate"])
            else:
                # Start a new evolution
                random.seed(3227)
                self.pop = self.toolbox.population(n=N_POP)
                start_gen = 0

            # # Evaluate the entire population
            for ind in self.pop:
                ind.fitness.values = self.toolbox.evaluate(ind)
        except BaseException as e:
            logging.error(f"gp_deap_adf_cp.run_gp restart / start ERROR: {e}")
            tb = ''.join(traceback.format_tb(e.__traceback__))
            logging.debug(f"gp_deap_adf_cp.run_gp ERROR: \n {tb}")

        try:
            # update population and stats
            self.hof.update(self.pop)
            self.record = self.stats.compile(self.pop)
            self.logbook.record(gen=0, evals=len(self.pop), **self.record)
            if self.verbose:
                logging.info(self.logbook.stream)
        except BaseException as e:
            logging.error(f"gp_deap_adf_cp.run_gp update population and stats ERROR: {e}")
            tb = ''.join(traceback.format_tb(e.__traceback__))
            logging.debug(f"gp_deap_adf_cp.run_gp ERROR: \n {tb}")


        filenamebase = self.checkpointfilepath.split(".")[0]

        generation_reached = 0
        try:
            for g in range(start_gen, N_GEN):
                generation_reached = g
                # Select the offspring
                try:
                    self.offspring = self.toolbox.select(self.pop,
                                                         len(self.pop))
                except BaseException as e:
                    logging.error(f"gp_deap_adf_cp.run_gp 'select' {e}")
                    tb = ''.join(traceback.format_tb(e.__traceback__))
                    logging.debug(f"gp_deap_adf_cp.run_gp 'select': \n {tb}")

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
                self.pop = self.offspring
                self.hof.update(self.pop)

                self.record = self.stats.compile(self.pop)
                try: # this stats.compile was throwing errors
                     # (not yet understood):
                    pass
                except:
                    pass

                self.logbook.record(gen=g, evals=len(invalids), **self.record)
                if self.verbose:
                    logging.info(self.logbook.stream)

                if g % CP_FREQ == 0 and g != 0:
                    # Fill the dictionary using the dict(key=value[, ...]) constructor
                    cp = dict(population=self.pop,
                            generation=g,
                            halloffame=self.hof,
                            logbook=self.logbook,
                            rndstate=random.getstate())

                    # set generation marked check point file:
                    if self.run_done_txt in filenamebase:
                        filenamebase = filenamebase[:-5]
                    num_to_mark = self.u.fix_number_for_sort(g) # add preceeding 0s
                    cp_file_g_marked = f"{filenamebase}_{num_to_mark}.pkl"

                    with open(cp_file_g_marked, "wb") as cp_file:
                        pickle.dump(cp, cp_file)

        except BaseException as e:
            logging.error(f"gp_deap_adf_cp.run_gp evolution mech {e}")
            tb = ''.join(traceback.format_tb(e.__traceback__))
            logging.debug(f"gp_deap_adf_cp.run_gp ERROR: \n {tb}")

        # checkpoint again after completing set generations:
        if self.run_done_txt in filenamebase:
            filenamebase = filenamebase[:-5]
        cp_done_file = f"{filenamebase}_{self.run_done_txt}.pkl"

        cp = dict(population=self.pop,
                        generation=generation_reached,
                        halloffame=self.hof,
                        logbook=self.logbook,
                        rndstate=random.getstate())
        with open(cp_done_file, "wb") as cp_file:
            pickle.dump(cp, cp_file)


        return self.pop, self.stats, self.hof, self.logbook

    def set_gp_params(self, params: dict):
        '''
        Now to handle ADFs with elistim too.
        Set the major parameters for genetic programming with Deap.

        Fitness function, Individual and GP tree base classes. Population,
        genetic operators, initiation of population mechanism.
        '''
        logging.debug(f"gp_deap_adf_cp.set_gp_params - ELITISM")
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
                                  no_of_elite=self.p.naut_dict['NO_OF_ELITE'],
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
                                no_of_elite,
                                tournsize):
        '''
        deap_users suggestion:
        https://groups.google.com/g/deap-users/c/iannnLI2ncE/m/eI4BcVcwFwMJ

        '''
        # selBest would be the obvious choice, but this assumes FitnessMin setup
        # therefore, selWorst to choose those individuals with highest fitness
        best = tools.selBest(individuals,
                             int(no_of_elite))

        tournament = tools.selTournament(individuals,
                                         int(k-no_of_elite),
                                         tournsize=tournsize)
        return best + tournament
