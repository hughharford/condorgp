from condorgp.learning.dependency_mocked import DependencyMocked
from condorgp.learning.dependency_factory import DependencyFactory


class DependencyFactoryOverloaded(DependencyFactory):
    def __init__(self):
        pass

    def get_dependency(self):
        return DependencyMocked()