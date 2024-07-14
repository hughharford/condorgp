import os
import os.path

import pytest
import logging
from pytest_bdd import scenarios, given, when, then, parsers

from tests.fixtures import *

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

  Scenario Outline: One living cell is run
    Given CellEvaluator and one cells
    When an evaluation is made
    Then one result are returned
    And this is handled

  Scenario Outline: Three living cells code are run
    Given CellEvaluator, 3 cells and a database
    When an evaluation is made
    Then 3 results are returned
    And these are stored in the database

"""

@given('GpControl with naut_06_gp_strategy')
def gpcontrol_n_naut_06(gpc):
    Factory().start_logger()

    gpc.use_adfs = 1
    pset = 'naut_pset_02_adf'
    p = 1
    g = 0
    cp_freq = g+1
    gpc.set_gp_n_cp(freq=cp_freq, cp_file="test12_done")
    gpc.setup_gp(pset_spec=pset, pop_size=p, no_gens=g)
    gpc.run_backtest = 1
    gpc.inject_strategy = 1

@when('a first evolved strategy run is made')
def first_gp_strategy_run(gpc):
    eval = 'eval_nautilus'
    gpc.set_test_evaluator(eval)
    gpc.run_gp()

@then('the initial strategy fitness is not zero')
def adf_fitness_is_not_zero(gpc):
    max_fitness_found = gpc.gp.logbook.select("max")[-1]
    logging.info(f'max_fitness_found = {max_fitness_found}')
    assert max_fitness_found > -21000
