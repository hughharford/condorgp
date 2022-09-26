import pytest
from condorgp.utils import Utils
from condorgp.deap_condor import CondorDeap

class UtilTest:
    def __init__(self) -> None:
        self.u = Utils()

@pytest.fixture
def utils():
    util = UtilTest()
    return util.u

class DeapTester:
    def __init__(self) -> None:
        self.ourdeap = CondorDeap()

@pytest.fixture
def deap_one():
    a = DeapTester()
    return a.ourdeap
