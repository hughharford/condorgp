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

import operator
import math
import random

import numpy

from condorgp.params import util_dict, test_dict, lean_dict
from condorgp.util.log import CondorLogger
from condorgp.evaluation.lean_runner import RunLean
from condorgp.factories.initial_factory import LocalFactory


class GpControl:
    def __init__(self):
        '''
            Here is where the gp is controlled from:

            Setup, sizing and initiation of gp runs
        '''
        self.inject_gp()
        self.inject_utils()
        self.inject_lean_runner()
        self.inject_logger()

        filler_INIT = '>'*10
        self.log.info(f"{filler_INIT}, {__class__} - DEAP gp - run began {filler_INIT}")

    def inject_gp(self):
        ''' dependency injection of gp '''
        self.gp = LocalFactory().get_gp_provider()

    def inject_utils(self):
        ''' dependency injection of utils '''
        self.util = LocalFactory().get_utils()

    def inject_lean_runner(self):
        ''' dependency injection of lean runner '''
        self.lean = LocalFactory().get_lean_runner()

    def inject_logger(self):
        ''' dependency injection of logger '''
        self.log = CondorLogger().get_logger()

    def setup_gp(self):
        ''' sets: 1. additional functions & terminals
                  2. major gp parameters
                  3: inputs for fitness evaluation
                  4: population size, defaults to 2 to test efficacy
                  5: the number of generations
                  6: the evaluator
                  7: the stats feedback
        '''
        # Set: 1. additional functions & terminals
        additional_funcs = {'name': 'protectedDiv',
                            'arrity': 2,
                            'method': self.protectedDiv}
        additional_terms = {}
        self.gp.set_pset(additional_funcs, additional_terms)

        # Set 2. major gp parameters
        params = {}
        self.gp.set_gp_params(params)

        # Sets 3: inputs for fitness evaluation
        inputs = {}
        self.gp.set_inputs(inputs)

        # Sets 4: population size, defaults to 2 to test efficacy
        self.pop_size = 1
        self.gp.set_pop_size(self.pop_size)

        # Set 5: the number of generations
        no_gens = 1
        self.gp.set_gens(no_gens)

        # Set 6: the evaluator
        self.gp.set_evaluator(self.evalIntoAndFromLean)

        # Set 7: the stats feedback
        stat_params = {}
        self.gp.set_stats(stat_params)

    def set_population(self, pop_size = 2):
        self.gp.set_pop_size(pop_size)

    def run_gp(self):
        ''' undertakes the run as specified'''
        self.gp.run_gp()

    def evalIntoAndFromLean(self, individual):
        # Transform the tree expression in a callable function
        func = self.gp.toolbox.compile(expr=individual)
        # output individual into Lean-ready class, for Lean evaluation

        # Lean evaluation: basic Lean run for now
        input_ind = 'IndBasicAlgo1'
        config_to_run = test_dict['CONDOR_TEST_CONFIG_FILE_1']

        self.util.copy_config_in(input_ind)
        self.util.copy_algo_in(input_ind)

        self.lean.run_lean_via_CLI(input_ind+'.py', config_to_run)

        Return_over_MDD = 'STATISTICS:: Return Over Maximum Drawdown'
        got = self.util.get_keyed_line_within_limits(Return_over_MDD)
        new_fitness = float(self.util.get_last_chars(got[0]))

        fill = '<*>'*6
        self.log.info(f'evalIntoAndFromLean, new fitness {fill}{new_fitness}')
        # returns a float in a tuple, i.e.
        #                               14736.68704775238,
        return new_fitness,

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

    def get_logbook(self):
        return self.gp.logbook

if __name__ == "__main__":
    c = GpControl()
    c.setup_gp()
    c.run_gp()
