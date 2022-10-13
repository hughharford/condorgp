import os

from condorgp.params import lean_dict, test_dict, highlevel_config_dict
from condorgp.util.utils import Utils
from condorgp.util.log import CondorLogger


class RunLean():
    def __init__(self) -> None:
        self.util = Utils()
        self.log = CondorLogger().get_logger()

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
        PATH = test_dict['CONDORGP_WITHIN_LEAN_DIR']
        ALGO_NAME = input_ind
        JSON_CONFIG = input_json
        try:
            if input_ind == "set":  ALGO_NAME = self.set_default_ind()
            elif input_ind == "test":   ALGO_NAME = self.set_test_ind()
            elif input_ind == "":   ALGO_NAME = 'main.py'

            if input_json == "set" or input_ind == "test":
                JSON_CONFIG = self.set_default_config_json() # input_json

            if highlevel_config_dict['RUN_VERBOSE_FOR_DEBUG']:
                os. chdir("../Lean/LocalPackages/condorgp")
                run_string = f"lean backtest {PATH}{ALGO_NAME} \
                            --lean-config {PATH}{JSON_CONFIG} \
                            --verbose"
                self.log.info(f"RUNNING:  {run_string}")
                os.system(run_string)
                os. chdir("../../../condorgp")
                self.util.cut_pys_in_backtest_code_dir() # tidy backtests / Results
                self.util.pull_latest_log_into_overall_backtest_log()
        except Exception as e:
            self.log.error(f'ERROR, lean_runner: {run_string}')

    def set_default_ind(self): # input_ind
        algo = test_dict['BASIC_TEST_ALGO_LEAN']
        self.util.cp_ind_to_lean_algos(test_dict['CONDOR_CONFIG_PATH'], algo)
        return algo

    def set_test_ind(self): # input_ind
        algo = test_dict['V1_TEST_ALGO_LEAN']
        self.util.cp_ind_to_lean_algos(test_dict['CONDOR_CONFIG_PATH'], algo)
        self.util.overwrite_main_with_input_ind(algo)
        return algo

    def set_default_config_json(self): # input_json
        json = test_dict['CONDOR_TEST_CONFIG_FILE_1']
        self.util.cp_config_to_lean_launcher(test_dict['CONDOR_CONFIG_PATH'], json)
        return json

if __name__ == "__main__":
    lean = RunLean()
    lean.run_lean_via_CLI()

    # lean.run_lean_via_CLI('test')
