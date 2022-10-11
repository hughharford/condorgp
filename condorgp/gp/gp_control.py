from condorgp.params import util_dict, test_dict, lean_dict

from condorgp.factories.initial_factory import InitialFactory
from condorgp.factories.custom_funcs_factory import CustomFuncsFactory

from condorgp.gp.gp_evaluators import GpEvaluators

class GpControl:
    def __init__(self):
        '''
            Here is where the gp is controlled from:

            Setup, sizing and initiation of gp runs:
                psets
                operators
                evaluator

            The major dependency is DEAP.
        '''
        self.inject_gp()
        self.inject_utils()
        self.inject_lean_runner()
        self.inject_logger()

        filler_INIT = '>'*10
        self.log.info(f"{filler_INIT}, {__class__} Initialising {filler_INIT}")

    def inject_gp(self):
        ''' dependency injection of gp '''
        cf = CustomFuncsFactory()
        self.gp_custom_funcs = cf.get_gp_custom_functions()

        lf = InitialFactory()
        self.gp = lf.get_gp_provider()
        self.gp_psets = lf.get_gp_psets(self.gp_custom_funcs)

    def inject_utils(self):
        ''' dependency injection of utils '''
        self.util = InitialFactory().get_utils()

    def inject_lean_runner(self):
        ''' dependency injection of lean runner '''
        self.lean = InitialFactory().get_lean_runner()

    def inject_logger(self):
        ''' dependency injection of logger '''
        self.log = InitialFactory().get_logger()

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
                            'method': self.gp_custom_funcs.protectedDiv}
        additional_terms = {}
        self.gp.set_defined_pset(self.gp_psets, "default_untyped", additional_funcs, additional_terms)

        # Set 2. major gp parameters
        params = {}
        self.gp.set_gp_params(params)

        # Sets 3: inputs for fitness evaluation
        inputs = {}
        self.gp.set_inputs(inputs)

        # Sets 4: population size, defaults to 2 to test efficacy
        self.pop_size = 2
        self.gp.set_pop_size(self.pop_size)

        # Set 5: the number of generations
        no_gens = 1
        self.gp.set_gens(no_gens)

        # Set 6: the evaluator
        self.gp.set_evaluator(self.evalIntoAndFromLean)

        # Set 7: the stats feedback
        stat_params = {}
        self.gp.set_stats(stat_params)

    def set_pset(self, pset_name = ''):
        ''' sets' the pset to default, unless input != '' '''
        return self.gp.set_defined_pset(self.gp_psets, pset_name)

    def set_population(self, pop_size = 2):
        self.gp.set_pop_size(pop_size)

    def set_generations(self, no_g = 1):
        self.gp.set_gens(no_g)

    def set_test_evaluator(self, use_this_evaluator = ''):
        '''
        default to eval_test_C, but
        can specify any evaluation function by string

        provided named function is within gp_control...
        '''
        if use_this_evaluator != '':
            new_evaluator = self.get_custom_evaluator(use_this_evaluator)
            if new_evaluator:
                print(new_evaluator, " type of this is: ", type(new_evaluator))
            self.gp.set_evaluator(new_evaluator)
        else:
            self.gp.set_evaluator(self.eval_test_5)


    def get_custom_evaluator(self, e_name):
        try:
            temp = eval('self.' + e_name)
            return temp
        except:
            print("get_custom_evaluator ERROR")
            return None

    def run_gp(self, inputs = [0,0,0]):
        ''' undertakes the run as specified'''
        self.gp.run_gp(inputs)

    def get_logbook(self):
        return self.gp.logbook

    def evalIntoAndFromLean(self, individual):
        # Transform the tree expression in a callable function
        func = self.gp.toolbox.compile(expr=individual)
        # output individual into Lean-ready class, for Lean evaluation

        # Lean evaluation: basic Lean run for now
        #### HSTH 09 10 ###
        input_ind = 'IndBasicAlgo1.py'
        config_to_run = test_dict['CONDOR_TEST_CONFIG_FILE_1']

        self.util.copy_config_in(input_ind)
        self.util.copy_algo_in(input_ind)

        self.lean.run_lean_via_CLI(input_ind, config_to_run)

        Return_over_MDD = 'STATISTICS:: Return Over Maximum Drawdown'
        got = self.util.get_keyed_line_in_limits(Return_over_MDD)
        new_fitness = float(self.util.get_last_chars(got[0]))

        fill = '<*>'*6
        self.log.info(f'evalIntoAndFromLean, new fitness {fill}{new_fitness}')
        # returns a float in a tuple, i.e.
        #                               14736.68704775238,
        return new_fitness,

    def eval_test_5_2(self, individual):
        # Transform the tree expression in a callable function
        func = self.gp.toolbox.compile(expr=individual)

        check_text = 'hello_world'
        self.log.info(f'eval_test_5_2, start: PRINT INDIVIDUAL >>> {individual}')
        try:
            self.log.info(f'eval_test_5_2, RUN? >>> {func(check_text)}')
            # now look for the intended output:
            log_file_path = util_dict['CONDOR_LOG']
            output = self.util.get_keyed_line_in_limits(check_text,
                                                log_file_n_path = log_file_path)
            # print(output)
            if check_text in output[0]:
                new_fitness = 100
            else:
                new_fitness = 0
        except BaseException as e:
            self.log.info(f'eval_test_5_2, ERROR >>> {e}')
            new_fitness = -10

        self.log.info(f'eval_test_5_2, set fitness: {new_fitness}')
        # returns a float in a tuple, i.e.
        #                               14736.68704775238,
        return new_fitness,

    def eval_test_5(self, individual):
        # Transform the tree expression in a callable function
        func = self.gp.toolbox.compile(expr=individual)

        self.log.info(f'eval_test_5, OUTPUTTING IND >>> \n {individual}')

        config_to_run = lean_dict['LEAN_INJECTED_ALGO_JSON']
        self.util.cp_injected_algo_in_and_sort('_test_05.py','')
        try:
            # not specifying: 'gpInjectAlgo_done.py'
            self.lean.run_lean_via_CLI('main.py', config_to_run)
            # algo set to main.py in lean_runner
        except BaseException as e:
            self.log.error("eval_test_5, attempting Lean run", str(e))

        new_fitness = 0
        self.log.info(f'eval_test_5, new fitness {new_fitness}')
        # returns a float in a tuple, i.e.
        #                               14736.68704775238,
        return new_fitness,

    def eval_test_6(self, individual):
        # Transform the tree expression in a callable function
        func = self.gp.toolbox.compile(expr=individual)

        self.log.info(f'eval_test_6, OUTPUTTING IND >>> \n {individual}')

        # additional code to inject (approaching from individual...)
        extant_line = '''
    def newly_injected_code(self):
        return ConstantAlphaModel(InsightType.Price,
                                  InsightDirection.Up,
                                  timedelta(minutes = 20),
                                  0.025, None
                                  )'''

        injected_line = extant_line
        if 'Alpha' in individual:
            injected_line = individual

        self.util.cp_injected_algo_in_and_sort('_test_06.py', str(individual))

        config_to_run = lean_dict['LEAN_INJECTED_ALGO_JSON']
        try:
            self.lean.run_lean_via_CLI('main.py', config_to_run)
        except BaseException as e:
            self.log.error("eval_test_6, attempting Lean run")

        # find fitness here:
        new_fitness = 0
        Return_over_MDD = 'STATISTICS:: Return Over Maximum Drawdown'
        got = self.util.get_keyed_line_in_limits(Return_over_MDD)
        new_fitness = float(self.util.get_last_chars(got[0]))

        self.log.info(f'eval_test_6, new fitness {new_fitness}')
        # returns a float in a tuple, i.e.
        #                               14736.68704775238,
        return new_fitness,

if __name__ == "__main__":
    eval_used = 'eval_test_5' # GpEvaluators().get_named_evaluator('eval_test_5') #
    pset_used = 'test_pset5c'
    c = GpControl()
    c.setup_gp()
    c.set_test_evaluator(eval_used)
    c.set_pset(pset_used)
    c.set_population(1)
    c.set_generations(1)
    c.run_gp()
    # max_fitness_found = c.gp.logbook.select("max")[-1]
    # print(max_fitness_found)
    print(f"DIRECT GpControl run, using: evaluator: {eval_used} , and pset: {pset_used}")
