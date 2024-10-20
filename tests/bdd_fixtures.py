import pytest
from condorgp.learning.dependency_injection.dependency_factory import DependencyFactory
from condorgp.learning.dependency_injection.dependency_factory_overridden import DependencyFactoryOverridden

@pytest.fixture
def dep_di():
    return DependencyFactory().get_dependency()

@pytest.fixture
def dep_di_mock():
    return DependencyFactoryOverridden().get_dependency()
