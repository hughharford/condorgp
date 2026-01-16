import pytest

from condorgp.params import Params
from condorgp.util.utils import Utils
from condorgp.factories.util_factory import UtilFactory

from condorgp.cells.cell_eval import CellEvaluator
from condorgp.cells.cell import Cell

@pytest.fixture
def cell_evaluator():
    return CellEvaluator()

@pytest.fixture
def cell_factory():
    return UtilFactory()

@pytest.fixture
def cell_central():
        return Cell()
