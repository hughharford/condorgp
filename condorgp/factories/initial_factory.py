from condorgp.utils import Utils
from condorgp.gp.gp_dependency import GpDependency

class LocalFactory:
    def __init__(self):
        pass

    def get_utils(self):
        return Utils()

    def get_gp_provider(self):
        return GpDependency()
