from condorgp.params import Params #, util_dict, test_dict, lean_dict

from condorgp.factories.initial_factory import InitialFactory
from condorgp.factories.custom_funcs_factory import CustomFuncsFactory

# NB
# TODO:below, search for: "### HACK HERE HACK HERE ###"

class GpControl:
    def __init__(self):
        # get params object:
        self.p = Params()
        '''
            Where the gp is controlled from.
            Setup, sizing, initiation of gp runs: psets, operators, evaluator
            The major dependency is DEAP.
        '''
        self.inject_gp() # inject dependencies
        self.inject_utils()
        self.inject_logger()
        self.inject_backtest_runner()

        self.log.info(f"{'>'*10}, GpControl Initialising {'>'*10}")
        # default population set and evaluator (fitness function)
        self.default_pset = 'default_untyped'
        self.default_eval = self.evalIntoAndFromLean
        self.default_tidyup = 1
        self.run_backtest = 1 # 1 = run lean in evaluation func, 0 = don't

    def inject_gp(self):
        ''' dependency injection of gp '''
        cf = CustomFuncsFactory()
        self.gp_custom_funcs = cf.get_gp_custom_functions()

        self.factory = InitialFactory()
        self.gp = self.factory.get_gp_provider()
        self.gp_psets = self.factory.get_gp_psets(self.gp_custom_funcs)
        self.gpf = self.factory.get_gp_funcs()

    def inject_utils(self):
        ''' dependency injection of utils '''
        self.util = self.factory.get_utils()

    def inject_backtest_runner(self):
        ''' dependency injection of backtest runner '''
        # was lean, now moving to Nautilus
        # this returns a Nautilus backtest base object, but below
        # this will be run via a hack command line script to capture
        # logs - as the core of Nautilus is in Rust (and logging connections)
        # are currently beyond me
        ### HACK HERE HACK HERE ###
        self.backtester = self.factory.get_backtest_runner(self.log)

    def inject_logger(self):
        ''' dependency injection of logger '''
        self.log = self.factory.get_logger()

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

        # LEAN:
        # additionally, copy gp_custom_functions to LEAN LocalPackages:
        # self.util.cp_custom_funcs_to_lp() # cf tidy up in run_gp, default on

    def set_population(self, pop_size):
        self.gp.set_pop_size(pop_size)

    def set_generations(self, no_g):
        self.gp.set_gens(no_g)

    def set_test_evaluator(self, new_eval = ''):
        '''
        default to eval_test_5, can spec any evaluation function by string
        provided named function is within gp_control...
        '''
        if new_eval:
            new_eval = self.get_custom_evaluator(new_eval)
            if new_eval: self.log.debug(f'GpControl set evaluator: {new_eval}')
            self.gp.set_evaluator(new_eval)
        else:
            self.gp.set_evaluator(self.eval_test_6)

    def get_custom_evaluator(self, e_name):
        try:
            return eval('self.' + e_name)
        except:
            self.log.error(f"GpControl get_custom_evaluator ERROR: {e_name}")
            return None

    def run_gp(self, inputs = [0,0,0]):
        ''' undertakes the run as specified'''
        self.gp.run_gp(inputs)
        # LEAN HANGOVER:
        # # # # # if self.default_tidyup: self.util.del_pys_from_local_packages()

    def get_logbook(self):
        return self.gp.logbook

    def evalIntoAndFromLean(self, individual):
        # Transform the tree expression in a callable function
        func = self.gp.toolbox.compile(expr=individual)
        # run Lean with algo and config:
        input_ind = 'IndBasicAlgo1.py'
        config_to_run = self.p.test_dict['CONDOR_TEST_CONFIG_FILE_1']
        self.util.copy_config_in(input_ind)
        self.util.copy_algo_in(input_ind)
        self.backtester.run_lean_via_CLI(input_ind, config_to_run)
        # get fitness
        Return_over_MDD = 'STATISTICS:: Return Over Maximum Drawdown'
        got = self.util.get_key_line_in_lim(Return_over_MDD)
        new_fitness = float(self.util.get_last_chars(got[0]))
        self.log.info(f'evalIntoAndFromLean, new fitness {new_fitness}')
        return new_fitness, # returns a float in a tuple, i.e. 16.6,

    def eval_test_5_2(self, individual):
        # Transform the tree expression in a callable function
        func = self.gp.toolbox.compile(expr=individual)
        new_fitness = 0
        check = 'hello_world'
        self.log.info(f'eval_test_5_2, PRINT INDIVIDUAL >>> {individual}')
        try:
            self.log.info(f'eval_test_5_2, RUN? >>> {func(check)}')
            log_file_path = self.p.util_dict['CONDOR_LOG']
            out = self.util.get_key_line_in_lim(
                                    check, log_filepath = log_file_path)
            if check in out[0]: new_fitness = 100
        except BaseException as e:
            self.log.info(f'eval_test_5_2, ERROR >>> {e}')
            new_fitness = -10
        self.log.info(f'eval_test_5_2, set fitness: {new_fitness}')
        return new_fitness,

    def eval_test_5(self, individual):
        # Transform the tree expression in a callable function
        func = self.gp.toolbox.compile(expr=individual)
        self.log.info(f'eval_test_5, OUTPUTTING IND >>> \n {individual}')
        new_fitness = 0
        config_to_run = self.p.lean_dict['LEAN_INJECTED_ALGO_JSON']
        self.util.cp_inject_algo_in_n_sort('_test_05.py','')
        try:
            self.backtester.run_lean_via_CLI('main.py', config_to_run)
        except BaseException as e:
            self.log.error("eval_test_5, attempting Lean run", str(e))
        self.log.info(f'eval_test_5, new fitness {new_fitness}')
        return new_fitness,

    def eval_test_6(self, individual):
        # Transform the tree expression in a callable function
        func = self.gp.toolbox.compile(expr=individual)
        self.log.info(f'eval_test_6, OUTPUTTING IND >>> \n {individual}')
        new_fitness = 0.0
        # additional code to inject (approaching from individual...)
        try:
            self.util.cp_inject_algo_in_n_sort('_test_06.py', str(individual))
        except Exception as e:
            self.log.debug(f'{individual} not wrapped: {str(e)}')
            new_fitness = -100.0
        config_to_run = self.p.lean_dict['LEAN_INJECTED_ALGO_JSON']
        try:
            if self.run_backtest:
                self.log.debug("GpControl.eval_test_6 >>>> RUN LEAN >>>>")
            # LEAN HANGOVER:
            # # # # # # # #
                self.backtester.run_lean_via_CLI('main.py', config_to_run)
                new_fitness = self.gpf.get_fit_6()
            else:
                self.log.debug("<< WOULD RUN LEAN HERE >>>>>>>>>>>>>>>>>>>>>>>")
        except BaseException as e:
            self.log.error("ERROR eval_test_6, attempting Lean run")

        self.log.info(f'eval_test_6, new fitness {new_fitness}')
        return new_fitness, # returns a float in a tuple, i.e.  14736.68,

    def eval_nautilus(self, individual):
        ''' First inclusion of Nautilus in evaluation function '''
        evalf_name = 'eval_nautilus'

        # Transform the tree expression in a callable function
        func = self.gp.toolbox.compile(expr=individual) # Deap requires this
        self.log.info(f'{evalf_name}, OUTPUTTING IND >>> \n {individual}')
        new_fitness = 0.0
        # additional code to inject evolved code individual
        try:
            # LEAN HANGOVER:
            # # # # # # # #
            # #
            # self.util.cp_inject_algo_in_n_sort('_test_06.py', str(individual))
            pass
            # would do something here, but kept out for now
        except Exception as e:
            self.log.debug(f'eval_nautilus: {individual} not wrapped: {str(e)}')
            new_fitness = -100.0

        try:
            if self.run_backtest:
                self.log.debug(f"GpControl.{evalf_name} >>>> RUN NAUTILUS >>>>")
                self.backtester.basic_run_through()
                new_fitness = self.gpf.get_fit_nautilus_1()
                self.log.debug(f"GpControl.{evalf_name} >>>> NAUTILUS fitness {new_fitness} >>>>")

            else:
                self.log.debug(f"<< ERROR eval_nautilus >>> RUN NAUTILUS HERE >>>>>>>>>>> {new_fitness}")
        except BaseException as e:
            self.log.error(f"ERROR {evalf_name}, attempting Nautilus run: {e}")

        self.log.info(f'GpControl.{evalf_name}, new fitness {new_fitness}')
        return new_fitness, # returns a float in a tuple, i.e.  14736.68,



if __name__ == "__main__":

    eval_used = 'eval_nautilus' # 'eval_test_6'
    pset_used = 'test_pset7aTyped'
    pop = 5
    gens = 2
    c = GpControl()
    c.setup_gp(pset_used, pop, gens)
    c.run_backtest = 1
    c.default_tidyup = 1
    c.set_test_evaluator(eval_used)
    c.run_gp()

    print('Hall of fame:')
    for x, individual in enumerate(c.gp.hof):
        print(c.gp.hof.items[x])

    print(c.gp.logbook)

    print(f"DIRECT GpControl run, using: \
          evaluator: {eval_used} , and pset: {pset_used}")
