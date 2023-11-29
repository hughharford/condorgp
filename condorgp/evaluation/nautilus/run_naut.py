import subprocess
import logging
from condorgp.params import Params
from condorgp.util.utils import Utils
from condorgp.util.log import CondorLogger

class RunNautilus():
    def __init__(self, script_to_run = "") -> None:

        self.utils = Utils()
        p = Params()
        self.util_dict = p.get_params("util_dict")
        self.test_dict = p.get_params("test_dict")
        self.naut_dict = p.get_params("naut_dict")

        self.naut_log = self.naut_dict['NAUTILUS_LOG_FILE']

        self.cmd_str = "python"
        self.eval_path = self.naut_dict['NAUTILUS_EVALUATION_PATH']
        if script_to_run != "":
            self.script_str = f"{self.eval_path}/{script_to_run}"
        else: # default if required:
            self.script_str = f"{self.eval_path}/naut_runner_03_egFX.py"

        logging.info(">> RunNautilus evaluation ready NAUTILUS >> ")


    def basic_run_through(self, specified_script: str = ""):
        '''
            Runs Nautilus script in a basically separated process.
        '''
        if specified_script != "": # use specified script for further runs
            self.script_str = f"{self.eval_path}/{specified_script}"
            
        result = ""
        if self.script_str:
            result = subprocess.run([self.cmd_str, self.script_str],
                                    stdout=subprocess.PIPE)
        else:
            logging.error("No Nautilus script provided")
        logging.info(">>> RunNautilus.basic_run_through DONE evaluating >>>")
        return result

if __name__ == "__main__":
    logging.info("Running RunNautilus")
    script_to_run = "naut_runner_03_egFX.py"
    n = RunNautilus(script_to_run = script_to_run)
    n.basic_run_through()
