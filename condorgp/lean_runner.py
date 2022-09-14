import os

from condorgp.params import lean_dict, test_dict, highlevel_config_dict
from condorgp.utils import cp_config_to_lean_launcher, cp_ind_to_lean_algos

class RunLean():
    def __init__(self) -> None:
        pass

    def adjust_config_specifics():
        '''
        For later:
            adjust the current_in_use_config.json for the
            specific algorithm file
        '''
        pass

    def run_lean_via_CLI(self, input_ind="set", input_json="set"):
        '''
        current Condorgp primary way to run lean fitness function.

            # this is the latest run format for Lean CLI
            # note how it runs in Lean/LocalPackages

        N.b. Can cut out use of Lean containers if required.
             In this case, tests will fail...
        Requires:
            1 - Algorithm to be set (manual .py name here for now)
            2 - Configuration json to be set (also manual for now)

        Both 1 & 2 are copied into place in the Lean package.
        Then the run command is made
        '''
        BACKTEST_PATH_LOCALPACKAGES = 'condorgp/Backtests/'

        JSON_PATH = test_dict['CONDORGP_WITHIN_LEAN_DIR']
        ALGO_PATH = test_dict['CONDORGP_WITHIN_LEAN_DIR']

        ALGO_NAME = input_ind
        JSON_CONFIG = input_json


        if input_ind == "set":
            ALGO_NAME = set_default_individual() # input_ind
        if input_json == "set":
            JSON_CONFIG = set_default_config_json() # input_json

        if highlevel_config_dict['RUN_VERBOSE_FOR_DEBUG']:
            os. chdir("../Lean/LocalPackages")
            os.system(f"lean backtest {ALGO_PATH}{ALGO_NAME} \
                        --lean-config {JSON_PATH}{JSON_CONFIG} \
                        --output {BACKTEST_PATH_LOCALPACKAGES} \
                        --verbose")
            os. chdir("../../condorgp")

def set_default_individual(): # input_ind
    algo_name = test_dict['BASIC_TEST_ALGO_LEAN']
    cp_ind_to_lean_algos(test_dict['CONDOR_CONFIG_PATH'], algo_name)
    return algo_name

def set_default_config_json(): # input_json
    f_json = test_dict['CONDOR_TEST_CONFIG_FILE_1']
    cp_config_to_lean_launcher(test_dict['CONDOR_CONFIG_PATH'], f_json)
    return f_json

if __name__ == "__main__":
    lean = RunLean()
    lean.run_lean_via_CLI('IndBasicAlgo1.py')
