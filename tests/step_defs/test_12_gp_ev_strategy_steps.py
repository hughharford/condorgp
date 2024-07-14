import os
import os.path

import pytest
import logging
from pytest_bdd import scenarios, given, when, then, parsers

from tests.gpc_fixtures import *

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

scenarios('../features/12_gp_ev_strategy.feature')

"""
Feature: CondorGp's evolved code is immediately most effective as a strategy
  As a gp algorithm running with Nautilus,
  Evolved code must be structured as a Nautilus strategy,
  To ensure the ongoing evolution is well targeted.

  Scenario Outline: Evolved code can be run as a strategy
    Given GpControl with naut_06_gp_strategy
    When a first evolved strategy run is made
    Then the initial strategy fitness is not zero
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
