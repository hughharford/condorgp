import numpy
import random
import logging
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

class GpDeapAdfCp(GpDeapADF):
    def __init__(self):
        '''
            Provides the workings for Deap to operate.
        '''
        super.__init__
        self.checkpointfile = None
        self.checkpoint_freq = None
        self.checkpointfilepath = None
        self.p = Params()
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

            # Evaluate the entire population
            for ind in self.pop:
                ind.fitness.values = self.toolbox.evaluate(ind)

        except BaseException as e:
            logging.error(f"gp_deap_adf_cp.run_gp restart / start ERROR: {e}")

        self.hof.update(self.pop)
        self.record = self.stats.compile(self.pop)
        self.logbook.record(gen=0, evals=len(self.pop), **self.record)
        if self.verbose:
            logging.info(self.logbook.stream)

        try:
            for g in range(start_gen, N_GEN):
                # Select the offspring
                self.offspring = self.toolbox.select(self.pop, len(self.pop))
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
                    filenamebase = self.checkpointfilepath.split(".")[0]
                    if self.run_done_txt in filenamebase:
                        filenamebase = filenamebase[:-5]
                    cp_file_g_marked = f"{filenamebase}_{g}.pkl"

                    with open(cp_file_g_marked, "wb") as cp_file:
                        pickle.dump(cp, cp_file)
        except BaseException as e:
            logging.error(f"gp_deap_adf_cp.run_gp evolution mech {e}")

        # checkpoint again after generations:
        cp_done_file = f"{filenamebase}_{self.run_done_txt}.pkl"
        cp = dict(population=self.pop,
                        generation=g,
                        halloffame=self.hof,
                        logbook=self.logbook,
                        rndstate=random.getstate())
        with open(cp_done_file, "wb") as cp_file:
            pickle.dump(cp, cp_file)


        return self.pop, self.stats, self.hof, self.logbook
