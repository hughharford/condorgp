import os
import os.path

import pytest
from pytest_bdd import scenarios, given, when, then, parsers

from tests.fixtures import *

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

pytest.gpc = None

scenarios('../features/09_gp_typed_adf.feature')

"""
Feature: GpControl's typed evolved code must be runnable
  As a gp algorithm,
  Evolved code must be typed, include ADFs, and be able to run,
  To ensure the code is of use.

  Scenario Outline: Evolved code can be run including ADFs
    Given GpControl with "<pset_ADF>"
    When a short ADF run is made with "<evaluator>"
    Then the fitness is not zero

    Examples:
      | pset_ADF            |   evaluator          |
      | naut_pset_02_adf    |   eval_nautilus      |
"""
@given(parsers.cfparse('GpControl with "{pset_ADF:String}"',
                        extra_types=EXTRA_TYPES), target_fixture='pset_ADF')
@given('GpControl with "<pset_ADF>"', target_fixture='<pset_ADF>')
def gpcontrol_with_typed_psets08(gpc, pset_ADF):
    p = 1
    g = 1
    gpc.use_adfs = 1
    gpc.select_gp_provider()
    gpc.setup_gp(pset_spec=pset_ADF, pop_size=p, no_gens=g)
    gpc.run_backtest = 1
    pytest.gpc = gpc

@when(parsers.cfparse('a short ADF run is made with "{evaluator:String}"',
                        extra_types=EXTRA_TYPES), target_fixture='evaluator')
@when('a short ADF run is made with "<evaluator>"', target_fixture='<evaluator>')
def first_ADF_run(evaluator):
    pytest.gpc.set_test_evaluator(evaluator)
    pytest.gpc.run_gp()

@then('the fitness is not zero')
def adf_fitness_is_not_zero(gpc):
    max_fitness_found = gpc.gp.logbook.select("max")[-1]
    # min_fitness_found = gpc.gp.logbook.select("min")[0]
    assert max_fitness_found != 0
