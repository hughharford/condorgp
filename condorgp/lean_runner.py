import os

from condorgp.params import lean_dict, test_dict, highlevel_config_dict
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

    def run_lean_via_CLI(self, input_ind, input_json):
        ''' simple but current Condorgp primary way to run lean fitness function.
        N.b. Can cut out use of Lean containers if required.
             In this case, tests will fail...
        Requires:
            1 - Algorithm to be set (manual .py name here for now)
            2 - Configuration json to be set (also manual for now)

        Both 1 & 2 are copied into place in the Lean package.
        Then the run command is made
        '''
        JSON_PATH = lean_dict['LEAN_CONFIG_DIR']
        ALGO_PATH = lean_dict['LEAN_ALGOS_FOLDER']
        ALGO_NAME_SIN_PY = input_ind
        JSON_CONFIG_INC_JSON = input_json

        # i.e. be able to cut out all usage of Lean containers if helpful
        if highlevel_config_dict['RUN_WITH_LEAN_CONTAINERS']:
            os. chdir("../Lean")
            os.system(f"lean backtest {ALGO_PATH}{ALGO_NAME_SIN_PY}.py --lean-config {JSON_PATH}{JSON_CONFIG_INC_JSON} --output Backtests")
            os. chdir("../condorgp")
        # --verbose

if __name__ == "__main__":
    lean = RunLean()
    lean.run_lean_via_CLI()
