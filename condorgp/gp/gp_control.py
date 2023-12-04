from condorgp.params import Params #, util_dict, test_dict, lean_dict
import logging
from condorgp.factories.initial_factory import InitialFactory
from condorgp.factories.custom_funcs_factory import CustomFuncsFactory
from condorgp.util.log import CondorLogger

from nautilus_trader.examples.strategies.ema_cross import EMACrossConfig


# NB
# TODO:below, search for: "### HACK HERE HACK HERE ###"

class GpControl:
    def __init__(self):
        '''
            Where the gp is controlled from.
            Setup, sizing, initiation of gp runs: psets, operators, evaluator
            The major dependency is DEAP.
        '''
        # get params object:
        self.p = Params()
        self.inject_gp() # inject dependencies
        self.inject_utils()
        self.initiate_logger()
        self.inject_backtest_runner()

        logging.info(f"{'>'*5}, GpControl Initialising {'>'*5}")
        # default population set and evaluator (fitness function)
        self.default_pset = 'default_untyped'
        self.default_eval = self.eval_nautilus
        self.run_backtest = 1 # 1 = run lean in evaluation func, 0 = don't

    def inject_gp(self):
        ''' dependency injection of gp '''
        cf = CustomFuncsFactory()
        self.gp_custom_funcs = cf.get_gp_custom_functions()
        self.factory = InitialFactory()
        self.gp = self.factory.get_gp_provider()
        self.gp_psets = self.factory.get_gp_psets(self.gp_custom_funcs)
        #  not using get_gp_naut_psets - separating out creates complications
        self.gpf = self.factory.get_gp_funcs()

    def inject_utils(self):
        ''' dependency injection of utils '''
        self.util = self.factory.get_utils()

    def inject_backtest_runner(self):
        ''' dependency injection of backtest runner '''
        ### HACK HERE HACK HERE ###
        default_script = "naut_runner_03_egFX.py"
        self.backtester = self.factory.get_backtest_runner(default_script)

    def initiate_logger(self):
        ''' dependency injection of logger '''
        self.factory.start_logger()

    def setup_gp(self, pset_spec = '', pop_size=2, no_gens=1):
        ''' sets: 1. additional functions & terminals
                  2. major gp parameters
                  3: inputs for fitness evaluation
                  4: population size, defaults to 2 to test efficacy
                  5: the number of generations
                  6: the evaluator
                  7: the stats feedback
        '''

        if pset_spec == '': pset_spec = self.default_pset
        funcs = {}     # Set: 1. additional functions & terminals
        terms = {}
        self.gp.set_defined_pset(self.gp_psets, pset_spec, funcs, terms)
        params = {}     # Set 2. major gp parameters
        self.gp.set_gp_params(params)
        inputs = {}     # Sets 3: inputs for fitness evaluation
        self.gp.set_inputs(inputs)
        self.pop_size = pop_size # Sets 4: population size, defaults to 2 for efficacy
        self.gp.set_pop_size(self.pop_size)
        self.gp.set_gens(no_gens)  # Set 5: the number of generations
        self.gp.set_evaluator(self.default_eval) # Set 6: the evaluator
        stat_params = {}        # Set 7: the stats feedback
        self.gp.set_stats(stat_params)

    def set_and_get_pset(self, pset_spec = ""):
        ''' sets a tailored pset '''
        if pset_spec == '': pset_spec = self.default_pset
        funcs = {}     # Set: 1. additional functions & terminals
        terms = {}
        self.gp.set_defined_pset(self.gp_psets, pset_spec, funcs, terms)
        return self.gp.pset

    def set_population(self, pop_size):
        self.gp.set_pop_size(pop_size)

    def set_generations(self, no_g):
        self.gp.set_gens(no_g)

    def set_test_evaluator(self, new_eval = ''):
        '''
        default to eval_test_6, can spec any evaluation function by string
        provided named function is within gp_control...
        '''
        if new_eval:
            new_eval = self.get_custom_evaluator(new_eval)
            if new_eval: logging.debug(f'GpControl set evaluator: {new_eval}')
            self.gp.set_evaluator(new_eval)
        else:
            self.gp.set_evaluator(self.eval_test_6)

    def get_custom_evaluator(self, e_name):
        try:
            return eval('self.' + e_name)
        except:
            logging.error(f"GpControl get_custom_evaluator ERROR: {e_name}")
            return None

    def run_gp(self, inputs = [0,0,0]):
        ''' undertakes the run as specified'''
        self.pop, self.stats, self.hof, self.logbook = self.gp.run_gp(inputs)

    def get_logbook(self):
        return self.gp.logbook

    def eval_nautilus(self, individual):
        '''
        First inclusion of Nautilus in evaluation function
        Set as the default evaluator, see gp_control.__init__
        '''
        evalf_name = 'eval_nautilus'
        # Transform the tree expression in a callable function
        func = self.gp.toolbox.compile(expr=individual) # Deap reqmt, not used
        new_fitness = 0.0
        try:
            if self.run_backtest:
                logging.debug(f"GpControl.{evalf_name} {'>'*2} RUN NAUTILUS")

                self.backtester.basic_run_through()
                new_fitness = self.gpf.get_fit_nautilus_1()

                # # logging.info(individual)
                # func = self.gp.toolbox.compile(expr=individual)
                # type_return = str(type(func))
                # # logging.info(type_return)
                # if 'nautilus_trader.examples.strategies.ema_cross.EMACrossConfig' in type_return:
                #     new_fitness = 100091
                # else:
                #     new_fitness = 191

                logging.debug(f"GpControl.{evalf_name} {'>'*2} "+
                              f"NAUTILUS fitness {new_fitness}")
            else:
                logging.debug(f"ERROR {evalf_name} {'>'*2} "+
                              f"NAUTILUS {'>'*4} {new_fitness}")
        except BaseException as e:
            logging.error(f"ERROR {evalf_name}, attempting Nautilus run: {e}")

        logging.info(f'GpControl.{evalf_name}, new fitness {new_fitness}')
        return new_fitness, # returns a float in a tuple, i.e.  14736.68,

if __name__ == "__main__":

    eval_used = 'eval_nautilus'
    pset_used = 'naut_pset_01' # 'test_pset5c'
    pop = 2
    gens = 1
    c = GpControl()
    c.setup_gp(pset_used, pop, gens)
    c.run_backtest = 1
    c.set_test_evaluator(eval_used)
    c.run_gp()

    print('Hall of fame:')
    for x, individual in enumerate(c.gp.hof):
        print(c.gp.hof.items[x])

    print(c.gp.logbook)

    print(f"DIRECT GpControl run, using: \
          evaluator: {eval_used} , and pset: {pset_used}")
