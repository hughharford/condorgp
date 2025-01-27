import subprocess
import logging
from condorgp.params import Params
from condorgp.util.utils import Utils

from nautilus_trader.model.identifiers import Venue
from nautilus_trader.test_kit.providers import TestInstrumentProvider
from condorgp.evaluation.get_strategies import GetStrategies
from condorgp.evaluation.naut_06_gp_strategy import NautRuns06GpStrategy
from condorgp.evaluation.naut_05_inject import NautRuns05Inject
from condorgp.evaluation.gp_strat_inj_01 import GpStratInject01

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

        logging.debug(">> RunNautilus evaluation ready NAUTILUS >> ")


    def basic_run(self,
                  specified_script: str="",
                  evolved_func="",
                  gp_strategy=False):
        '''
            In dev: Run Nautilus with evolved strategy provided.
            Recent: Run Nautilus with evolved config provided, more directly.
            Most basic: Runs Nautilus script in a separated process.
        '''
        result = 0.1

        if gp_strategy: # set GpControl: gpc.inject_strategy = 1
            logging.debug(">>> RunNautilus.basic_run naut_06_gp_strategy >>>")
            try:
                nrun = NautRuns06GpStrategy()
                nrun.main(evolved_strategy=evolved_func)
                logging.info(
                    ">>> RunNautilus.basic_run naut_06_gp_strategy ran >>>")
            except BaseException as e:
                logging.error(
                    f"ERROR {__name__}, failed basic_run gp_strategy: {e}")
        else:
            if evolved_func: # enable config_func into Nautilus evaluation:
                logging.debug(">>> RunNautilus.basic_run naut_05_inject >>>")
                nrun = NautRuns05Inject()
                try:
                    nrun.main(evolved_config=evolved_func)
                    logging.info(">>> RunNautilus.basic_run naut_05_inject ran >>>")
                except BaseException as e:
                    logging.error(
                        f"ERROR {__name__}, failed basic_run evolved_func: {e}")
            else:
                # run without injecting code, i.e. a script in a sub-process
                if specified_script != "": # use specified script for further runs
                    self.script_str = f"{self.eval_path}{specified_script}"
                else:
                    self.script_str = self.n_runner_inc_path

                if self.script_str:
                    result = subprocess.run([self.cmd_str, self.script_str],
                                            stdout=subprocess.PIPE)
                else:
                    logging.error("No Nautilus script provided")
        logging.debug(">>> RunNautilus.basic_run DONE evaluating >>>")
        return result

if __name__ == "__main__":
    logging.info("Running RunNautilus")
    script_to_run = "naut_03_egFX.py"
    n = RunNautilus()
    n.basic_run(evolved_func="12345", gp_strategy=True)
