import os.path

import pytest
import logging
from pytest_bdd import scenarios, given, when, then, parsers

from condorgp.params import Params
from condorgp.cell import Cell
# from tests.cell_fixtures import *
# from tests.cell_fixtures import CellEvaluator, UtilFactory

''' FEATURE DESCRIPTION:
Feature: CondorGp's evolved cell code needs basic operations
  As a gp algorithm with living cell structures,
  Evolved cells must be able to be added and removed, and a count kept
  To allow sensible management of cells.
'''

# EXTRA_TYPES = {
#     'Number': int,
#     'String': str,
#     'Float': float,
# }

# CONVERTERS = {
#     'initial': int,
#     'some': int,
#     'total': int,
# }

KEEPER = []

scenarios('../features/002_cell_basics.feature')

'''
# birth of a cell
  Scenario Outline: A cell is added
    Given no cells
    When a cell is born
    Then an object of type Cell is added
    And with first birth cell count is 1
'''


@given('no cells')
def given_no_cells():
    '''Given no cells'''
    assert Cell.get_cell_count() == 0

@when('a cell is born')
def when_a_cell_is_born():
    '''When a cell is born'''
    c1 = Cell(new_cell_ref="001", new_cell_type="PROTOTYPE")
    assert c1
    KEEPER.append(c1)

@then('an object of type Cell is added')
def then_an_object_of_type_cell_is_added():
    '''Then an object of type Cell is added'''
    assert type(KEEPER[0]) == Cell

@then('with first birth cell count is 1')
def and_with_first_birth_cell_count_is_1():
    assert Cell.get_cell_count() == 1

# TODO: other feature in test_002_cell_basics
'''
# death of a cell
  Scenario Outline: One living cell is run
    Given 1 extant cell
    When the cell is removed
    Then there are 0 objects of type Cell
    And with first removal cell count is 0 again
'''
