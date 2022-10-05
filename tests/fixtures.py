import pytest
from condorgp.utils import Utils
from condorgp.gp_control import GpControl
from condorgp.learning.dependency_factory import DependencyFactory
from condorgp.learning.dependency_factory_overridden import DependencyFactoryOverridden

@pytest.fixture
def utils():
    return Utils()

@pytest.fixture
def deap_one():
    return GpControl()

@pytest.fixture
def deap_two():
    return GpControl()

@pytest.fixture
def dep_di():
    return DependencyFactory().get_dependency()

@pytest.fixture
def dep_di_mock():
    return DependencyFactoryOverridden().get_dependency()
