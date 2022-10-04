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

# from deap import algorithms
from deap import base
# from deap import creator
# from deap import tools
from deap import gp

from condorgp.utils import Utils
from condorgp.params import util_dict, test_dict, lean_dict
from condorgp.util.log import CondorLogger
from condorgp.lean_runner import RunLean
from condorgp.factories.initial_factory import LocalFactory


class CondorDeap:
    def __init__(self):
        '''
            Setup the gp run
        '''
        self.util = Utils()

        # logging
        logger = CondorLogger()
        self.log = logger.get_logger()
        filler_INIT = '>'*10
        self.log.info(f"{filler_INIT}, {__class__} - DEAP gp - run began {filler_INIT}")

        lf = LocalFactory()
        self.gp = lf.get_gp_provider()

    def setup_gp(self):
        ''' sets additional functions & terminals '''
        additional_funcs = {'name': 'protectedDiv',
                            'arrity': 2,
                            'method': self.protectedDiv}
        additional_terms = {}
        self.gp.set_pset(additional_funcs, additional_terms)
        self.pset = self.gp.get_pset() # geeting this back to enable eval func


    def setup_gp_params(self, params = {}):
        ''' sets major gp parameters'''
        self.gp.set_gp_params(params)

    def setup_inputs(self, inputs = {}):
        ''' sets inputs for fitness evaluation'''
        self.gp.set_inputs(inputs)

    def setup_pop_size(self, pop_size = 2):
        ''' sets the population size, defaults to 2 to test efficacy'''
        self.gp.set_pop_size(pop_size)

    def setup_no_gens(self, no_gens = 1):
        ''' sets the number of generations'''
        self.gp.set_gens(no_gens)

    def setup_evaluator(self):
        self.gp.set_evaluator(self.evalIntoAndFromLean)

    def setup_stats(self, stat_params = {}):
        self.gp.set_stats(stat_params)

    def run_gp(self):
        ''' undertakes the run as specified'''
        self.gp.run_gp()

    def evalIntoAndFromLean(self, individual):
        # Transform the tree expression in a callable function
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
        # ERROR CAUSED HERE
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
        # this line alone worked when DEAP setup in this class:  func = self.toolbox.compile(expr=individual)
        # self.toolbox = base.Toolbox()
        # self.toolbox.register("compile", gp.compile, pset=self.pset)

        func = self.toolbox.compile(expr=individual)
        # output individual into Lean-ready class, for Lean evaluation

        # Lean evaluation: basic Lean run for now
        input_ind = 'IndBasicAlgo1'
        config_to_run = ''
        if input_ind[-1] == '1':
            config_to_run = test_dict['CONDOR_TEST_CONFIG_FILE_1']
        elif input_ind[-1] == '2':
            config_to_run = test_dict['CONDOR_TEST_CONFIG_FILE_2']

        self.util.copy_config_in(input_ind)
        self.util.copy_algo_in(input_ind)

        lean = RunLean()
        lean.run_lean_via_CLI(input_ind+'.py', config_to_run)

        Return_over_MDD = 'STATISTICS:: Return Over Maximum Drawdown'
        got = self.util.get_keyed_line_within_limits(Return_over_MDD)
        new_fitness = float(self.util.get_last_chars(got[0]))

        fill = '<*>'*6
        print(f'new fitness {fill}{new_fitness}')
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

def main():
    c = CondorDeap()
    c.setup_gp()
    c.setup_gp_params()
    c.setup_inputs()
    c.setup_pop_size(1)
    c.setup_no_gens()
    c.setup_evaluator()
    c.setup_stats()
    c.run_gp()

if __name__ == "__main__":
    main()

##### PREVIOUSLY:
#     # run gp, outputting population, stats, hall of fame:
#     ccc = CondorDeap()
# #    ccc.run()

#     # SAMPLE RUN
#     ccc.set_population(1)
#     pop, stats, mstats, hof, logbook = ccc.do_run(3)
#     # see what we got:
#     ccc.log.info('Hall of fame:')
#     for x, individual in enumerate(hof):
#         ccc.log.info(hof.items[x])

#     # Stats does not have the fitness data, just the stats functions
#     # print(ccc.stats.__dict__)
#     # print(ccc.stats.fields[0])

#     print()

#     # logbook:
#     print(f'logbook: \n {logbook}')

#     print()

#     # mstats
#     print(f'mstats: \n {mstats}')
