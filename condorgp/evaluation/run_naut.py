import subprocess
import logging
from condorgp.params import Params
from condorgp.util.utils import Utils
from condorgp.util.log import CondorLogger

from nautilus_trader.model.identifiers import Venue
from nautilus_trader.test_kit.providers import TestInstrumentProvider
from condorgp.evaluation.nautilus.get_strategies import GetStrategies
from condorgp.evaluation.nautilus.naut_05_inject import NautRunsEvolved

class RunNautilus():
    def __init__(self, script_to_run = "") -> None:

        self.utils = Utils()
        p = Params()
        self.util_dict = p.get_params("util_dict")
        self.test_dict = p.get_params("test_dict")
        self.naut_dict = p.get_params("naut_dict")

        self.naut_log = self.naut_dict['NAUTILUS_LOG_FILE']

        self.cmd_str = "python"
        self.eval_path = self.naut_dict['NAUTILUS_EVAL_PATH']
        if script_to_run != "":
            self.script_str = f"{self.eval_path}/{script_to_run}"
        else: # default if required:
            self.script_str = f"{self.eval_path}/naut_run_03_egFX.py"

        logging.info(">> RunNautilus evaluation ready NAUTILUS >> ")


    def basic_run_through(self, specified_script: str="", config_func=""):
        '''
            Runs Nautilus script in a basically separated process - early doors.
            Or secondarily, with config provided, more directly.
        '''
        result = 2

        if config_func:

            # enable config_func into Nautilus evaluation:

            # SIM = Venue("SIM")
            # AUDUSD_SIM = TestInstrumentProvider.default_fx_ccy("AUD/USD", SIM)

            # naut_config = GetStrategies(instrument = AUDUSD_SIM)
            # config = naut_config.get_config_strategy_without_full_declaration()

            nrun = NautRunsEvolved().get_strategy(config_func=config_func)

        else:
            # rn the old way, without injecting code
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
    script_to_run = "naut_run_03_egFX.py"
    n = RunNautilus(script_to_run = script_to_run)
    n.basic_run_through()
