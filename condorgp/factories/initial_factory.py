from condorgp.params import Params
from condorgp.util.utils import Utils
from condorgp.gp.gp_deap import GpDeap

from condorgp.gp.gp_psets import GpPsets
from condorgp.gp.gp_functions import GpFunctions
from condorgp.evaluation.run_naut import RunNautilus

from condorgp.util.log import CondorLogger

class InitialFactory():
    def __init__(self):
        pass

    def get_utils(self):
        return Utils()

    def get_gp_provider(self):
        return GpDeap()

    def get_gp_psets(self, customfuncs):
        return GpPsets(customfuncs)

    def get_gp_funcs(self):
        return GpFunctions()

    def get_backtest_runner(self):
        return RunNautilus()

    def start_logger(self):
        CondorLogger()

    def get_params(self):
        return Params()
