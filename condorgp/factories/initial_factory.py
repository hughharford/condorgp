from condorgp.util.utils import Utils
from condorgp.gp.gp_deap import GpDeap

from condorgp.gp.gp_psets import GpPsets
from condorgp.gp.gp_functions import GpFunctions
from condorgp.evaluation.nautilus.run_naut import RunNautilus

from condorgp.util.log import CondorLogger

class InitialFactory:
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

    def get_backtest_runner(self, logger):
        return RunNautilus(logger)
        # OLD return NautilusBTBase()
        # OLD return RunLean()

    def get_logger(self):
        return CondorLogger().get_logger()
