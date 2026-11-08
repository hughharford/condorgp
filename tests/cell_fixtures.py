import pytest

from condorgp.params import Params
from condorgp.util.utils import Utils
from condorgp.factories.util_factory import UtilFactory

from condorgp.cell.cell_evaluator import CellEvaluator


@pytest.fixture
def cell_evaluator():
    return CellEvaluator()

@pytest.fixture
def cell_factory():
    return UtilFactory()
