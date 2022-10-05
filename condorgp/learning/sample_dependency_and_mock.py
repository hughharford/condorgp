

from condorgp.learning.dependency_factory import DependencyFactory
from condorgp.learning.dependency_factory_overridden import DependencyFactoryOverridden



if __name__ == "__main__":
    input = 7
    actual_dep = DependencyFactory().get_dependency()
    print("Actual, adding: " + str(actual_dep.dep_add(input)))
    print("Actual, multiplying: " + str(actual_dep.dep_multiply(input)))

    mocked_dep = DependencyFactoryOverridden().get_dependency()
    print("Mocked, adding: " + str(mocked_dep.dep_add(input)))
    print("Mocked, multiplying: " + str(mocked_dep.dep_multiply(input)))
