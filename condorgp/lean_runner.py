import os

from condorgp.params import lean_dict, test_dict #
from condorgp.utils import copy_config_json_to_lean_launcher_dir, copy_ind_to_lean_algos_dir

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

    def run_lean_via_CLI(self, input_ind):
        ''' simple but current Condorgp primary way to run lean fitness function.

        Requires:
            1 - Algorithm to be set (manual .py name here for now)
            2 - Configuration json to be set (also manual for now)

        Both 1 & 2 are copied into place in the Lean package.
        Then the run command is made
        '''
        # # copy algo py into place
        # copy_ind_to_lean_algos_dir(
        #     test_dict['CONDOR_CONFIG_PATH'],
        #     'IndBasicAlgo1.py')

        # # copy .json across:
        # copy_config_json_to_lean_launcher_dir(
        #     test_dict['CONDOR_CONFIG_PATH'],
        #     test_dict['CONDOR_TEST_CONFIG_FILE'])

        JSON_PATH = ''
        ALGO_PATH = lean_dict['LEAN_ALGOS_FOLDER']
        # ALGO_NAME_SIN_PY = 'IndBasicAlgo1'
        ALGO_NAME_SIN_PY = input_ind

        os. chdir("../Lean")
        # os.system(f"lean backtest {ALGO_PATH}{ALGO_NAME_SIN_PY}.py --lean-config {JSON_PATH}config_test_condor.json --output Backtests")
        os. chdir("../condorgp")

        # --verbose


if __name__ == "__main__":
    lean = RunLean()
    lean.run_lean_via_CLI()
