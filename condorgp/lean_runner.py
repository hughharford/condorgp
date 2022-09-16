import os

from condorgp.params import lean_dict, test_dict, highlevel_config_dict
from condorgp.utils import cp_config_to_lean_launcher
from condorgp.utils import cp_ind_to_lean_algos
from condorgp.utils import overwrite_main_with_input_ind
from condorgp.utils import cut_pys_from_latest_backtests_code_dir
from condorgp.utils import pull_latest_log_into_overall_backtest_log

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

        JSON_PATH = test_dict['CONDORGP_WITHIN_LEAN_DIR']
        ALGO_PATH = test_dict['CONDORGP_WITHIN_LEAN_DIR']

        ALGO_NAME = input_ind
        JSON_CONFIG = input_json


        if input_ind == "set":
            ALGO_NAME = set_default_individual() # input_ind
        elif input_ind == "test":
            ALGO_NAME = set_test_individual()
        if input_json == "set" or input_ind == "test":
            JSON_CONFIG = set_default_config_json() # input_json

        if highlevel_config_dict['RUN_VERBOSE_FOR_DEBUG']:
            os. chdir("../Lean/LocalPackages/condorgp")
            os.system(f"lean backtest {ALGO_PATH}{ALGO_NAME} \
                        --lean-config {JSON_PATH}{JSON_CONFIG} \
                        --verbose")
            os. chdir("../../../condorgp")

            # tidy and get what our needs from backtests / Results output
            cut_pys_from_latest_backtests_code_dir()
            pull_latest_log_into_overall_backtest_log()

            # --output {BACKTEST_PATH_LOCALPACKAGES} \
                # taking out output specification, to control output tree repetition
            # BACKTEST_PATH_LOCALPACKAGES = 'Results'
            # test_dict['CONDORGP_WITHIN_LEAN_DIR']
            # tried the following:
            #                   '../../LocalPackages/condorgp/Results/'
            #                   '../../LocalPackages/condorgp/Results'
            #                   'Results'
            #                   './'
            #                   '.'
            #                   'Backtests'
            #                   '/Backtests'
            #                   '../../'
            #                   '../..'
            #                   ''



def set_default_individual(): # input_ind
    algo_name = test_dict['BASIC_TEST_ALGO_LEAN']
    cp_ind_to_lean_algos(test_dict['CONDOR_CONFIG_PATH'], algo_name)
    return algo_name

def set_test_individual(): # input_ind
    algo_name = test_dict['V1_TEST_ALGO_LEAN']
    cp_ind_to_lean_algos(test_dict['CONDOR_CONFIG_PATH'], algo_name)
    overwrite_main_with_input_ind(algo_name)
    return algo_name

def set_default_config_json(): # input_json
    f_json = test_dict['CONDOR_TEST_CONFIG_FILE_1']
    cp_config_to_lean_launcher(test_dict['CONDOR_CONFIG_PATH'], f_json)
    return f_json

if __name__ == "__main__":
    lean = RunLean()
    lean.run_lean_via_CLI()

    # lean.run_lean_via_CLI('test')
