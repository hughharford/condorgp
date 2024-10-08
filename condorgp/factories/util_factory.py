from condorgp.params import Params
from condorgp.util.utils import Utils
from condorgp.util.log import CondorLogger

class UtilFactory():
    def __init__(self):
        pass

    def get_utils(self):
        return Utils()

    def start_logger(self):
        CondorLogger()

    def get_params(self):
        return Params()
