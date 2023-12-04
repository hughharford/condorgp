import pytest
from condorgp.params import Params
from condorgp.util.utils import Utils
from condorgp.gp.gp_control import GpControl
from condorgp.learning.dependency_factory import DependencyFactory
from condorgp.learning.dependency_factory_overridden import DependencyFactoryOverridden
from condorgp.factories.initial_factory import InitialFactory


@pytest.fixture
def initial_factory():
    return InitialFactory()

@pytest.fixture
def params():
    return Params()

@pytest.fixture
def utils():
    return Utils()

@pytest.fixture
def gp_control(): 
    return GpControl()

@pytest.fixture
def dep_di():
    return DependencyFactory().get_dependency()

@pytest.fixture
def dep_di_mock():
    return DependencyFactoryOverridden().get_dependency()
