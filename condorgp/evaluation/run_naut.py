import subprocess
import logging
from condorgp.params import Params
from condorgp.util.utils import Utils

from nautilus_trader.model.identifiers import Venue
from nautilus_trader.test_kit.providers import TestInstrumentProvider
from condorgp.evaluation.get_strategies import GetStrategies
from condorgp.evaluation.naut_05_inject import NautRunsEvolved

class RunNautilus():
    def __init__(self) -> None:

        self.utils = Utils()
        p = Params()
        self.util_dict = p.get_params("util_dict")
        self.test_dict = p.get_params("test_dict")
        self.naut_dict = p.get_params("naut_dict")

        self.naut_log = self.naut_dict['NAUTILUS_LOG_FILE']
        self.n_runner_inc_path = self.naut_dict['N_DEFAULT_RUN_INC_PATH']

        self.cmd_str = "python"
        self.eval_path = self.naut_dict['NAUTILUS_EVAL_PATH']

        logging.info(">> RunNautilus evaluation ready NAUTILUS >> ")


    def basic_run(self, specified_script: str="", evolved_func=""):
        '''
            Runs Nautilus script in a basically separated process - early doors.
            Or secondarily, with config provided, more directly.
        '''
        result = 0.1

        if evolved_func:
            # enable config_func into Nautilus evaluation:
            logging.info(">>> RunNautilus.basic_run + CONFIG_FUNC >>>")
            try:
                nrun = NautRunsEvolved()
                nrun.main(evolved_config=evolved_func)
                logging.info(">>> RunNautilus.basic_run CONFIG_FUNC ran >>>")
            except BaseException as e:
                logging.error(f"ERROR {__name__}, failed basic_run: {e}")
        else:
            # run without injecting code
            if specified_script != "": # use specified script for further runs
                self.script_str = f"{self.eval_path}{specified_script}"
            else:
                self.script_str = self.n_runner_inc_path

            if self.script_str:
                result = subprocess.run([self.cmd_str, self.script_str],
                                        stdout=subprocess.PIPE)
            else:
                logging.error("No Nautilus script provided")
        logging.info(">>> RunNautilus.basic_run DONE evaluating >>>")
        return result

if __name__ == "__main__":
    logging.info("Running RunNautilus")
    script_to_run = "naut_03_egFX.py"
    n = RunNautilus()
    n.basic_run()
