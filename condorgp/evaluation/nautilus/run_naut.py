import subprocess
from condorgp.params import naut_dict
from condorgp.util.utils import Utils
from condorgp.factories.initial_factory import InitialFactory


class RunNautilus():
    def __init__(self) -> None:
        self.f = InitialFactory()
        self.log = self.f.get_logger()
        self.utils = Utils()

        naut_log = naut_dict['NAUT_LOG_FILE']

        cmd_str = "/home/hsth/.pyenv/versions/3.10.8/envs/nautilus/bin/python"
        script_str = f"/home/hsth/code/hughharford/nautilus/condorgp/condorgp/evaluation/nautilus/nautilus_bt_base.py"
        log_file = "/home/hsth/code/hughharford/nautilus/condorgp/condorgp/util/logs/nautilus_log.txt"

        self.log.info(">>>> >>>> >>>> RunNautilus >>>> evaluating NAUTILUS HERE >>>> ")

        result = subprocess.run([cmd_str, script_str],
                                stdout=subprocess.PIPE)
        formatted_result = result.stdout.decode('utf-8')

        # self.log.info(formatted_result) # no need for this, Nautilus log goes
            # to nautilus_log.txt see utils.write_to_file
        self.utils.write_to_file(naut_log, formatted_result, mode = "a")
        # instead:
        self.log.info(">>>> >>>> >>>> RunNautilus >>>> DONE evaluating NAUTILUS HERE >>>> ")


if __name__ == "__main__":
    n = RunNautilus()
