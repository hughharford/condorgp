import pytest


from condorgp.params import Params
from condorgp.util.utils import Utils
from condorgp.factories.factory import Factory

from condorgp.gp.gp_functions import GpFunctions
from condorgp.gp.gp_control import GpControl

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
