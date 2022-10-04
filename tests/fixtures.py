import pytest
from condorgp.utils import Utils
from condorgp.deap_condor import CondorDeap
from condorgp.learning.dependency import Dependency

@pytest.fixture
def utils():
    return Utils()

@pytest.fixture
def deap_one():
    return CondorDeap()

@pytest.fixture
def get_dependency1():
    a = Dependency()
    return a
