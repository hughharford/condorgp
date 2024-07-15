import os
import os.path

import pytest
import logging
from pytest_bdd import scenarios, given, when, then, parsers

# from tests.cell_fixtures import *
# from tests.cell_fixtures import CellEvaluator, UtilFactory

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

scenarios('../features/001_cell_eval.feature')

"""
  Scenario Outline: Evolved living cell code is run
    Given CellEvaluator and no cells
    When an evaluation is made
    Then zero results are returned
    And this is handled
"""


@given('CellEvaluator and no cells')
def cell_eval_no_cells(cell_evaluator):
    # UtilFactory().start_logger()

    assert cell_evaluator.get_all_for_score()

@when('an evaluation is made')
def this_evaluation_is_made(cell_evaluator):
    assert cell_evaluator

@then('the initial strategy fitness is not zero')
def adf_fitness_is_not_zero(gpc):
    max_fitness_found = gpc.gp.logbook.select("max")[-1]
    logging.info(f'max_fitness_found = {max_fitness_found}')
    assert max_fitness_found > -21000


"""
#   Scenario Outline: One living cell is run
#     Given CellEvaluator and one cells
#     When an evaluation is made
#     Then one result are returned
#     And this is handled

#   Scenario Outline: Three living cells code are run
#     Given CellEvaluator, 3 cells and a database
#     When an evaluation is made
#     Then 3 results are returned
#     And these are stored in the database

"""
