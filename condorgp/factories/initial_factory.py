from condorgp.utils import Utils
from condorgp.gp.gp_deap import GpDeap
from condorgp.evaluation.lean_runner import RunLean
from condorgp.util.log import CondorLogger
class LocalFactory:
    def __init__(self):
        pass

    def get_utils(self):
        return Utils()

    def get_gp_provider(self):
        return GpDeap()

    def get_lean_runner(self):
        return RunLean()

    def get_logger(self):
        return CondorLogger()
