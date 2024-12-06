import time
import logging
import traceback
import math
import random

from condorgp.params import Params #, util_dict, test_dict, lean_dict
from condorgp.factories.factory import Factory

from nautilus_trader.examples.strategies.ema_cross import EMACrossConfig

class GpControl:
    def __init__(self):
        '''
            The Genetic Programming (gp) controller.

            Setup, sizing, initiation of gp runs: psets, operators, evaluator.
            The major dependency is DEAP.
        '''
        try:
            logging.info(f"{'>'*5}, GpControl Initialising {'>'*5}")

            # default population set and evaluator (fitness function)
            self.default_pset = 'naut_pset_01'
            self.default_eval = self.eval_nautilus
            self.run_backtest = 1
            self.verbose = 1 # default to print out
            # gather resources
            self.p = Params()
            self.factory = Factory()
            self.initiate_logger()
            self.inject_utils()
            self.keep_logs_tidy()
            self.inject_backtest_runner()

            self.randomised_test_fitness = 0 # default to evaluated fitness
            self.checkpointing = None # default to None. i.e. not using
            self.use_adfs = 0 # default to zero. i.e. not using
            self.inject_strategy = 0 # assume not

            logging.debug(f"GpControl: __init__ complete")
        except BaseException as e:
            logging.error(f"GPC ERROR: {e}")
            tb = ''.join(traceback.format_tb(e.__traceback__))
            logging.debug(f"GPC: {tb}")

    def set_gp_n_cp(self, freq, cp_file:str):
        ''' setup variables for DEAP checkpointing with gp_deap_adf_cp'''
        try:
            if not cp_file:
                raise ValueError(f"cp_file missing: set_gp_n_cp.")
            if freq > 0:
                self.checkpointing = 1
            self.inject_gp() # to establish self.gpc first
            self.gp.checkpoint_freq = freq
            self.run_done_txt = self.p.naut_dict['RUN_DONE_TEXT']
            self.gp.checkpointfile = cp_file + '.pkl'
            cp_path = self.p.naut_dict['CHECKPOINT_PATH']
            self.gp.checkpointfilepath = cp_path + self.gp.checkpointfile
            logging.info(f"GpControl - will checkpoint @ {freq}g's.")
            logging.debug(f"GpControl: set checkpointing complete")
        except BaseException as e:
            logging.error(f"gpc.set_gp_n_cp: {e}")
            tb = ''.join(traceback.format_tb(e.__traceback__))
            logging.debug(f"gpc.set_gp_n_cp: {tb}")

    def select_gp_provider_for_ADFs(self):
        ''' to be called for ADF without Checkpointing'''
        self.inject_gp()

    def inject_gp(self):
        ''' dependency injection of gp '''
        # getting gp_provider (varies)
        try:
            if self.checkpointing:
                self.gp = self.factory.get_gp_adf_cp_provider()
            elif self.use_adfs:
                self.gp = self.factory.get_gp_adf_provider()
            else:
                self.gp = self.factory.get_gp_provider()
            self.gp_psets_cls = self.factory.get_gp_psets() # get gp_psets
            self.gpf = self.factory.get_gp_funcs() # get gp_functions
            logging.debug(f"GpControl: inject_gp complete")
        except BaseException as e:
            logging.error(f"gpc.inject_gp ERROR: {e}")
            tb = ''.join(traceback.format_tb(e.__traceback__))
            logging.debug(f"gpc.inject_gp: {tb}")

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
        try:
            # set verbosity in gp:
            self.gp.verbose = self.verbose

            if pset_spec == '': pset_spec = self.default_pset
            funcs = {}     # Set: 1. additional functions & terminals
            terms = {}
            logging.debug(f"GpControl: set_defined_pset {pset_spec}")

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
        except BaseException as e:
            logging.error(f"GpControl SETUP_GP: {e}")
            tb = ''.join(traceback.format_tb(e.__traceback__))
            logging.debug(f"GpControl SETUP_GP: {tb}")

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
            tb = ''.join(traceback.format_tb(e.__traceback__))
            logging.debug(f"GpControl: {tb}")

        # show logbook
        logging.info(' deap __ Logbook:')
        logging.info(f"\n{self.gp.logbook}")

    def get_logbook(self):
        return self.gp.logbook

    def eval_nautilus(self, individual):
        '''
        First inclusion of Nautilus in evaluation function
        Set as the default evaluator, see gp_control.__init__
        '''
        set_backtest_id = "naut-run-06"
        evalf_name = 'eval_nautilus'
        # Transform the tree expression in a callable function
        func = self.gp.toolbox.compile(expr=individual)
        if self.verbose:
            printed_ind = [str(tree) for tree in individual]
            logging.debug(f" >>> eval_nautilus individual: {printed_ind}")
        new_fitness = 0.0
        if self.inject_strategy == 1: # new inject gp strategy approach
            new_fitness = -9988
            if self.run_backtest:
                logging.debug(f"GpControl.{evalf_name} {'>'*2} RUN NAUTILUS")
                self.backtester.basic_run(evolved_func=func, gp_strategy=True)
                new_fitness = self.gpf.find_fitness(
                                       backtest_id=set_backtest_id)
            else:
                logging.debug(f"ERROR {evalf_name} {'>'*2} "+
                              f"NAUTILUS {'>'*4} {new_fitness}")

        else:  # first inject gp strategy config approach
            try:
                if self.run_backtest:
                    logging.debug(
                        f"GpControl.{evalf_name} {'>'*2} RUN NAUTILUS")
                    self.backtester.basic_run(evolved_func=func)
                    new_fitness = self.gpf.find_fitness(
                                           backtest_id=set_backtest_id)
                elif self.randomised_test_fitness == 1:
                    new_fitness = random.uniform(0, 1)
                else:
                    logging.debug(f"ERROR {evalf_name} {'>'*2} "+
                                f"NAUTILUS {'>'*4} {new_fitness}")
            except BaseException as e:
                logging.error(
                    f"ERROR {evalf_name}, attempting Nautilus run: {e}")
                tb = ''.join(traceback.format_tb(e.__traceback__))
                logging.debug(f"eval_nautilus: {tb}")

        if self.verbose:
            logging.info(f'GpControl.{evalf_name}, new fitness {new_fitness}')
        return new_fitness, # returns a float in a tuple, i.e.  14736.68,

    def evalSymbRegTest(self, individual):
        # Transform the tree expression in a callable function
        func = self.gp.toolbox.compile(expr=individual)
        # Evaluate the sum of squared difference between the expression
        # and the real function : x**4 + x**3 + x**2 + x
        try:
            values = (x/10. for x in range(-10, 10))
            diff_func = lambda x: (func(x)-(x**4 + x**3 + x**2 + x))**2
            diff = sum(map(diff_func, values))
        except BaseException as e:
            # logging.error(f'evalSymbRegTest ERROR {e}')
            # tb = ''.join(traceback.format_tb(e.__traceback__))
            # logging.debug(f"evalSymbRegTest: {tb}")
            return -110.0, # return 110.0 when evolved func fails
        return diff,

    def undertake_run(self, gpc=None):
        start_time = time.time()

        if not gpc: gpc = GpControl()
        else:       gpc = gpc

        gpc.verbose = 1
        gpc.use_adfs = 1
        if gpc.use_adfs:
            pset_used = 'naut_pset_05_strategy' # 'naut_pset_04_strategy' # 'naut_pset_03_strategy'
            # 'naut_pset_02_adf' # 'test_adf_symbreg_pset' # 'test_pset5b'
        else:
            pset_used = 'naut_pset_01' #  'test_pset5b'
        eval_used = 'eval_nautilus' # evalSymbRegTest

        p = 20
        g = 2 # even
        cp_base = "240811_ev_cfg_fitness"
        if not g%2==0:
            err_note = f'g (no. generations) is odd, adjust: gpc.undertaken run'
            logging.error(err_note)
            raise ValueError(err_note)
        cp_freq = g/2
        gpc.set_gp_n_cp(freq=cp_freq, cp_file=cp_base+"")

        # gpc.select_gp_provider_for_ADFs() # call to use ADFs but not checkpoints
        gpc.setup_gp(pset_spec=pset_used, pop_size=p, no_gens=g)
        gpc.set_test_evaluator(eval_used)

        gpc.run_backtest = 0
        gpc.inject_strategy = 1 # set to 1, this selects naut_06_gp_strategy

        gpc.run_gp()

        # tidy up
        # CUT THIS FOR NOW, CONFUSING ERROR ON PIKA CONTAINER RUNNING...
        # Does question, is this really needed?
        #        gpc.util.tidy_cp_files(cp_base)

        if gpc.verbose:
            logging.info(' deap __ Hall of fame:')
            for x, individual in enumerate(gpc.gp.hof):
                printed_ind = [str(tree) for tree in gpc.gp.hof.items[x]]
                logging.info(f" deap generated individual: {printed_ind}")

        logging.debug(f"GpControl run, evaluator: {eval_used}, pset: {pset_used}")

        if gpc.run_backtest == 1:
            best = gpc.gp.hof.items[0]
            printed_ind = [str(tree) for tree in best]
            logging.info(f" Evolution run, best individual: \n\
                {printed_ind} __ fitness: {round(best.fitness,4)}")

        logging.info("--- %s seconds ---" % (round((time.time() - start_time),3)))

if __name__ == "__main__":
    gpc = GpControl()
    gpc.undertake_run()
