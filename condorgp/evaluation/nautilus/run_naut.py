import subprocess
from condorgp.params import Params
from condorgp.util.utils import Utils
# from condorgp.factories.initial_factory import InitialFactory


class RunNautilus():
    def __init__(self, logger, script_to_run = "") -> None:
        # self.factory = InitialFactory()
        # self.log = self.factory.get_logger()
        self.log = logger
        self.utils = Utils()
        p = Params()
        self.util_dict = p.get_params("util_dict")
        self.test_dict = p.get_params("test_dict")
        self.naut_dict = p.get_params("naut_dict")

        self.naut_log = self.naut_dict['NAUTILUS_LOG_FILE']

        self.cmd_str = "python"
        evaluation_path = self.naut_dict['NAUTILUS_EVALUATION_PATH']
        if script_to_run != "":
            self.script_str = f"{evaluation_path}/{script_to_run}"
        else: # default if required:
            self.script_str = "" #f"{evaluation_path}/naut_runner_03_egFX.py"

        if hasattr(self.log,'info'):
             self.log.info(">>>> >>>> RunNautilus.__init__ >>>> evaluating NAUTILUS >>>> ")


    def basic_run_through(self):
        '''
            Runs Nautilus script in a basically separated process.
        '''
        if self.script_str:
            result = subprocess.run([self.cmd_str, self.script_str],
                                    stdout=subprocess.PIPE)
        elif hasattr(self.log,'error'):
            self.log.error("No Nautilus script provided")

        if hasattr(self.log,'info'):
            self.log.info(">>>> >>>> RunNautilus.basic_run_through > DONE evaluating NAUTILUS >>>> ")


if __name__ == "__main__":
    from condorgp.factories.initial_factory import InitialFactory
    factory = InitialFactory()
    logger = factory.get_logger()

    print("Running RunNautilus")
    script_to_run = "naut_runner_03_egFX.py"
    n = RunNautilus(logger = logger, script_to_run = script_to_run)
    n.basic_run_through()
