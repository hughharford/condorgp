from condorgp.params import util_dict, test_dict, lean_dict

from condorgp.factories.initial_factory import InitialFactory
from condorgp.factories.custom_funcs_factory import CustomFuncsFactory

class GpControl:
    def __init__(self):
        '''
            Here is where the gp is controlled from.
            Setup, sizing, initiation of gp runs: psets, operators, evaluator
            The major dependency is DEAP.
        '''
        self.inject_gp() # inject dependencies
        self.inject_utils()
        self.inject_lean_runner()
        self.inject_logger()

        self.log.info(f"{'>'*10}, GpControl Initialising {'>'*10}")
        # default population set and evaluator (fitness function)
        self.default_pset = 'default_untyped'
        self.default_eval = self.evalIntoAndFromLean
        self.run_lean = 1 # 1 = run lean in evaluation func, 0 = don't

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

    def inject_lean_runner(self):
        ''' dependency injection of lean runner '''
        self.lean = self.factory.get_lean_runner()

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

    def get_logbook(self):
        return self.gp.logbook

    def evalIntoAndFromLean(self, individual):
        # Transform the tree expression in a callable function
        func = self.gp.toolbox.compile(expr=individual)
        # run Lean with algo and config:
        input_ind = 'IndBasicAlgo1.py'
        config_to_run = test_dict['CONDOR_TEST_CONFIG_FILE_1']
        self.util.copy_config_in(input_ind)
        self.util.copy_algo_in(input_ind)
        self.lean.run_lean_via_CLI(input_ind, config_to_run)
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
            log_file_path = util_dict['CONDOR_LOG']
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
        config_to_run = lean_dict['LEAN_INJECTED_ALGO_JSON']
        self.util.cp_inject_algo_in_n_sort('_test_05.py','')
        try:
            self.lean.run_lean_via_CLI('main.py', config_to_run)
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
        except:
            self.log.debug(f'{individual} not wrapped')
            new_fitness = -100.0
        config_to_run = lean_dict['LEAN_INJECTED_ALGO_JSON']
        try:
            if self.run_lean:
                self.log.debug("GpControl.eval_test_6 >>>> RUN LEAN >>>>")
                self.lean.run_lean_via_CLI('main.py', config_to_run)
                new_fitness = self.gpf.get_fit_6()
            else:
                self.log.debug("<< WOULD RUN LEAN HERE >>>>>>>>>>>>>>>>>>>>>>>")
        except BaseException as e:
            self.log.error("ERROR eval_test_6, attempting Lean run")

        self.log.info(f'eval_test_6, new fitness {new_fitness}')
        return new_fitness, # returns a float in a tuple, i.e.  14736.68,

if __name__ == "__main__":

    eval_used = 'eval_test_6'
    pset_used = 'test_pset6b'
    pop = 2
    gens = 1
    c = GpControl()
    c.setup_gp(pset_used, pop, gens)
    c.run_lean = 1
    c.set_test_evaluator(eval_used)
    c.run_gp()

    print(f"DIRECT GpControl run, using: \
          evaluator: {eval_used} , and pset: {pset_used}")
