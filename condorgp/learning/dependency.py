
class Dependency:
    def __init__(self) -> None:
        self.dependency = 1000

    def dep_multiply(self, x):
        return x * self.dependency

    def dep_add(self, x):
        return x + self.dependency
