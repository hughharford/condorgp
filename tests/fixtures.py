import pytest
from condorgp.params import Params
from condorgp.util.utils import Utils
from condorgp.gp.gp_control import GpControl
from condorgp.gp.gp_functions import GpFunctions
from condorgp.learning.dependency_injection.dependency_factory import DependencyFactory
from condorgp.learning.dependency_injection.dependency_factory_overridden import DependencyFactoryOverridden
from condorgp.factories.factory import Factory


@pytest.fixture
def initial_factory():
    return Factory()

@pytest.fixture
def params():
    return Params()

@pytest.fixture
def utils():
    return Utils()

@pytest.fixture
def gpf():
    return GpFunctions()

@pytest.fixture
def gp_control():
    return GpControl()

@pytest.fixture
def gpc():
    return GpControl()

@pytest.fixture
def dep_di():
    return DependencyFactory().get_dependency()

@pytest.fixture
def dep_di_mock():
    return DependencyFactoryOverridden().get_dependency()
