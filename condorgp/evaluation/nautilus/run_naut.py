import subprocess
from condorgp.params import naut_dict
from condorgp.util.utils import Utils
# from condorgp.factories.initial_factory import InitialFactory


class RunNautilus():
    def __init__(self, logger) -> None:
        # self.factory = InitialFactory()
        # self.log = self.factory.get_logger()
        self.log = logger
        self.utils = Utils()

        self.naut_log = naut_dict['NAUTILUS_LOG_FILE']

        self.cmd_str = "/home/hsth/.pyenv/versions/3.10.8/envs/nautilus/bin/python"
        self.script_str = f"/home/hsth/code/hughharford/nautilus/condorgp/condorgp/evaluation/nautilus/nautilus_bt_base.py"

        self.log.info(">>>> >>>> RunNautilus.__init__ >>>> evaluating NAUTILUS >>>> ")


    def basic_run_through(self):
        result = subprocess.run([self.cmd_str, self.script_str],
                                stdout=subprocess.PIPE)
        formatted_result = result.stdout.decode('utf-8')

        self.utils.write_to_file(self.naut_log, formatted_result, mode = "a")
        # self.log.info(formatted_result) # no need for this, Nautilus log goes
            # to nautilus_log.txt see utils.write_to_file
            # instead:
        self.log.info(">>>> >>>> RunNautilus.basic_run_through > DONE evaluating NAUTILUS >>>> ")


if __name__ == "__main__":
    from condorgp.factories.initial_factory import InitialFactory
    logger = InitialFactory().get_logger()
    n = RunNautilus(logger)
    n.basic_run_through()