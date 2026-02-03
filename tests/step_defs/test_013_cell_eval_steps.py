import os
import os.path

import pytest
import logging
from pytest_bdd import scenarios, given, when, then, parsers

from tests.cell_fixtures import cells

''' FEATURE DESCRIPTION:
Feature: CondorGp's evolved cell code needs evaluation
  As a gp algorithm running with living cell structures,
  Evolved cell code must be structured correctly,
  To allow evaluation via scoring.

'''

EXTRA_TYPES = {
    'Number': int,
    'String': str,
    'Float': float,
}

CONVERTERS = {
    'initial': int,
    'some': int,
    'total': int,
}

scenarios('../features/013_cell_eval.feature')

@given('CellEvaluator and no cells')
def cell_eval_no_cells(cells):
    assert not cells.get_all_for_score()

@when('an evaluation is made')
def this_evaluation_is_made(cells):
    assert cells

@then('zero results are returned')
def zero_length_result(cells):
    assert len(cells.get_all_for_score()) == 0

@then('this is handled')
def zero_length_handled():
    pass

"""
#   Scenario Outline: One living cell is run
#     Given CellEvaluator and one cell
#     When an evaluation is made
#     Then one result are returned
#     And this is handled

#   Scenario Outline: Three living cells code are run
#     Given CellEvaluator, 3 cells and a database
#     When an evaluation is made
#     Then 3 results are returned
#     And these are stored in the database

"""
