import pytest

from condorgp.params import Params
from condorgp.util.utils import Utils
from condorgp.factories.factory_util import UtilFactory

from condorgp.evaluation.cell.cell_eval import CellEvaluator

@pytest.fixture
def cell_evaluator():
    return CellEvaluator()

@pytest.fixture
def cell_factory():
    return UtilFactory()
