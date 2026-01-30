import pytest

from condorgp.params import Params
from condorgp.util.utils import Utils
from condorgp.factories.util_factory import UtilFactory

from condorgp.cells.cell import Cell
from condorgp.cells.cells import Cells

@pytest.fixture
def cell_factory():
    return UtilFactory()

@pytest.fixture
def cell():
    return Cell()

@pytest.fixture
def cells():
    return Cells()
