from condorgp.learning.dependency_injection.dependency import Dependency

class DependencyMocked(Dependency):
    def __init__(self) -> None:
        self.dependency = 5000

    def dep_multiply(self, x):
        return x*self.dependency
