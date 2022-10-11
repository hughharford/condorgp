from condorgp.params import util_dict, test_dict, lean_dict
from condorgp.factories.initial_factory import InitialFactory
from condorgp.factories.custom_funcs_factory import CustomFuncsFactory

class GpEvaluators:
    '''
    An attempt to get evaluator definition out of gp_control.
    Proving difficult to get to work
    '''

    def __init__(self):
        cf = CustomFuncsFactory()
        self.gp_custom_funcs = cf.get_gp_custom_functions()

        factory = InitialFactory()
        self.gp = factory.get_gp_provider()

        self.gp_psets = factory.get_gp_psets(self.gp_custom_funcs)
        additional_funcs = {}
        additional_terms = {}
        self.gp.set_defined_pset(self.gp_psets, "default_untyped",
                                 additional_funcs, additional_terms)
        params = {}
        self.gp.set_gp_params(params)
        # self.individual = self.gp.toolbox.individual # cover for evaluator params

    def get_named_evaluator(self, named_evaluator):
        try:
            return eval('self.' + named_evaluator + '(self.gp.toolbox.individual)')
        except Exception as e:
            print("GpEvaluators ERROR: " + str(e))
            return None


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

if __name__ == "__main__":
    e = GpEvaluators()
    e.eval_test_5
