from condorgp.params import Params
from condorgp.util.utils import Utils
from condorgp.gp.gp_deap import GpDeap
from condorgp.gp.gp_deap_adf import GpDeapADF
from condorgp.gp.gp_deap_adf_cp import GpDeapAdfCp

from condorgp.gp.gp_psets import GpPsets
from condorgp.gp.gp_functions import GpFunctions
from condorgp.evaluation.run_naut import RunNautilus

from condorgp.util.log import CondorLogger

class Factory():
    def __init__(self):
        pass

    def get_utils(self):
        return Utils()

    def get_gp_provider(self):
        return GpDeap()

    def get_gp_adf_provider(self):
        return GpDeapADF()

    def get_gp_adf_cp_provider(self):
        return GpDeapAdfCp()

    def get_gp_psets(self):
        return GpPsets()

    def get_gp_funcs(self):
        return GpFunctions()

    def get_backtest_runner(self):
        return RunNautilus()

    def start_logger(self):
        CondorLogger()

    def get_params(self):
        return Params()
