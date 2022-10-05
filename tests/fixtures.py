import pytest
from condorgp.utils import Utils
from condorgp.gp_control import GpControl
from condorgp.learning.dependency import Dependency

@pytest.fixture
def utils():
    return Utils()

@pytest.fixture
def deap_one():
    return GpControl()

@pytest.fixture
def get_dependency1():
    a = Dependency()
    return a
