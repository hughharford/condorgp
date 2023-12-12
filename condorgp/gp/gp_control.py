import time
import logging

from condorgp.params import Params #, util_dict, test_dict, lean_dict
from condorgp.factories.factory import Factory
from condorgp.factories.custom_funcs_factory import CustomFuncsFactory

from nautilus_trader.examples.strategies.ema_cross import EMACrossConfig

class GpControl:
    def __init__(self):
        '''
            The Genetic Programming (gp) controller.
            Setup, sizing, initiation of gp runs: psets, operators, evaluator.
            The major dependency is DEAP.
        '''
        logging.info(f"{'>'*5}, GpControl Initialising {'>'*5}")

        # default population set and evaluator (fitness function)
        self.default_pset = 'naut_pset_01'
        self.default_eval = self.eval_nautilus
        self.run_backtest = 1
        # gather resources
        self.p = Params()
        self.factory = Factory()
        self.initiate_logger()
        self.inject_utils()
        self.keep_logs_tidy()
        self.inject_backtest_runner()

        self.use_adfs = 0 # default to zero. i.e. not using
        if self.use_adfs == 0:
            self.inject_gp() # call via select_gp_provider if adfs in use

        logging.debug(f"GpControl: __init__ complete")

    def select_gp_provider(self):
        self.inject_gp()

    def inject_gp(self):
        ''' dependency injection of gp '''
        cf = CustomFuncsFactory()
        self.gp_custom_funcs = cf.get_gp_custom_functions()
        if self.use_adfs:
            self.gp = self.factory.get_gp_adf_provider()
        else:
            self.gp = self.factory.get_gp_provider()
        self.gp_psets_cls = self.factory.get_gp_psets(self.gp_custom_funcs)
        #  not using get_gp_naut_psets - separating out creates complications
        self.gpf = self.factory.get_gp_funcs()
        logging.debug(f"GpControl: inject_gp complete")

    def inject_utils(self):
        ''' dependency injection of utils '''
        self.util = self.factory.get_utils()

    def inject_backtest_runner(self):
        ''' dependency injection of backtest runner '''
        self.backtester = self.factory.get_backtest_runner()

    def initiate_logger(self):
        ''' dependency injection of logger '''
        self.factory.start_logger()

    def keep_logs_tidy(self):
        ''' keep logs tidy: '''
        nautlog = self.p.naut_dict['NAUTILUS_LOG_FILE']
        self.util.keep_x_lines_of_log(log_file_path=nautlog,
                                      no_last_lines=10000)
        self.util.make_no_log_backups(log_file_path=nautlog,
                                      no_backups=2)

    def setup_gp(self, pset_spec='', pop_size=2, no_gens=1):
        ''' sets: 1. additional functions & terminals
                  2. major gp parameters
                  3: inputs for fitness evaluation
                  4: population size, defaults to 2 to test efficacy
                  5: the number of generations
                  6: the evaluator
                  7: the stats feedback
        '''
        logging.debug(f"GpControl: starting setup_gp {'>'*8}")

        if pset_spec == '': pset_spec = self.default_pset
        funcs = {}     # Set: 1. additional functions & terminals
        terms = {}
        self.gp.set_defined_pset(self.gp_psets_cls, pset_spec, funcs, terms)
        logging.debug(f"GpControl: set_defined_pset complete")

        params = {}     # Set 2. major gp parameters
        self.gp.set_gp_params(params)
        logging.debug(f"GpControl: set_gp_params complete")

        inputs = {}     # Sets 3: inputs for fitness evaluation
        self.gp.set_inputs(inputs)
        logging.debug(f"GpControl: set_inputs complete")

        self.pop_size = pop_size # Sets 4: population size, defaults to 2 for efficacy
        self.gp.set_pop_size(pop_size)
        logging.debug(f"GpControl: set_pop_size complete")

        self.gp.set_gens(no_gens)  # Set 5: the number of generations
        self.gp.set_evaluator(self.default_eval) # Set 6: the evaluator
        logging.debug(f"GpControl: set_evaluator complete")

        stat_params = {}        # Set 7: the stats feedback
        self.gp.set_stats(stat_params)
        logging.debug(f"GpControl: set_stats complete")

        logging.debug(f"GpControl: complete SETUP_GP {'>'*8}")

    def set_and_get_pset(self, pset_spec = ""):
        ''' get and set a tailored pset '''
        if pset_spec == '': pset_spec = self.default_pset
        funcs = {}     # Set: 1. additional functions & terminals
        terms = {}
        self.gp.set_defined_pset(self.gp_psets_cls, pset_spec, funcs, terms)
        return self.gp.pset

    def set_population(self, pop_size):
        self.gp.set_pop_size(pop_size)

    def set_generations(self, no_g):
        self.gp.set_gens(no_g)

    def set_test_evaluator(self, new_eval = ''):
        '''
        default to eval_nautilus, can spec any evaluation function by string
        provided named function is within gp_control...
        '''
        if new_eval:
            new_eval = self.get_custom_evaluator(new_eval)
            if new_eval:
                logging.debug(f'GpControl set evaluator: {new_eval.__name__}')
            self.gp.set_evaluator(new_eval)
        else:
            self.gp.set_evaluator(self.eval_nautilus)

    def get_custom_evaluator(self, e_name):
        try:
            return eval('self.' + e_name)
        except:
            logging.error(f"GpControl get_custom_evaluator ERROR: {e_name}")
            return None

    def run_gp(self, inputs = [0,0,0]):
        ''' undertakes the run as specified'''
        logging.debug(f"GpControl: starting GP run now {'_'*10}")
        try:
            if self.use_adfs:
                self.pop, self.stats, self.hof, self.logbook = self.gp.run_gp(inputs)
            else:
                self.pop, self.stats, self.hof, self.logbook = self.gp.run_gp()
        except BaseException as e:
            logging.error(f"GpControl ERROR: {e}")

        # show logbook
        logging.info(' deap __ Logbook:')
        logging.info(self.gp.logbook)

    def get_logbook(self):
        return self.gp.logbook

    def eval_nautilus(self, individual):
        '''
        First inclusion of Nautilus in evaluation function
        Set as the default evaluator, see gp_control.__init__
        '''
        evalf_name = 'eval_nautilus'
        # Transform the tree expression in a callable function
        func = self.gp.toolbox.compile(expr=individual)
        printed_ind = [str(tree) for tree in individual]
        logging.info(f" >>> eval_nautilus individual: {printed_ind}")
        new_fitness = 0.0
        try:
            if self.run_backtest:
                logging.debug(f"GpControl.{evalf_name} {'>'*2} RUN NAUTILUS")
                self.backtester.basic_run(evolved_func=func)
                new_fitness = self.gpf.find_fitness()
            else:
                logging.debug(f"ERROR {evalf_name} {'>'*2} "+
                              f"NAUTILUS {'>'*4} {new_fitness}")
        except BaseException as e:
            logging.error(f"ERROR {evalf_name}, attempting Nautilus run: {e}")

        logging.info(f'GpControl.{evalf_name}, new fitness {new_fitness}')
        return new_fitness, # returns a float in a tuple, i.e.  14736.68,

if __name__ == "__main__":
    start_time = time.time()

    gpc = GpControl()

    gpc.use_adfs = 1
    if gpc.use_adfs:
        pset_used = 'naut_pset_02_adf'
    else:
        pset_used = 'naut_pset_01' #  'test_pset5c'
    eval_used = 'eval_nautilus'

    newpop = 1
    gens = 1

    gpc.select_gp_provider()
    gpc.setup_gp(pset_spec=pset_used, pop_size=newpop, no_gens=gens)
    gpc.set_test_evaluator(eval_used)
    gpc.run_backtest = 1
    gpc.run_gp()
    logging.info(' deap __ Hall of fame:')
    for x, individual in enumerate(gpc.gp.hof):
        printed_ind = [str(tree) for tree in gpc.gp.hof.items[x]]
        logging.info(f" deap generated individual: {printed_ind}")

    # now in gpc.run_gp
    # logging.info(' deap __ Logbook:')
    # logging.info(gpc.gp.logbook)

    logging.info(f"DIRECT GpControl run, using: \
          evaluator: {eval_used} , and pset: {pset_used}")

    logging.info("--- %s seconds ---" % (time.time() - start_time))
