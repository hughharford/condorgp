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
pytest.f_max = []
pytest.f_min = []

scenarios('../features/08_gp_fitmax.feature')

"""
  Scenario Outline: Evolved code shows fitness improvement
    Given GpControl is run with "<pset>"
    When run with evaluator "<evaluator>"
    Then either max fitness improves over the generations
    And or min fitness improves over generations

  Examples:
    |  pset         |   evaluator          |
    |  naut_pset_01 |   eval_nautilus      |
"""

@given(parsers.cfparse('GpControl is run with "{pset:String}"',
                       extra_types=EXTRA_TYPES), target_fixture='pset')
@given('GpControl is run with "<pset>"')
def gpcontrol_run_001(gpc, pset):
    p = 5
    g = 3
    gpc.setup_gp(pset_spec=pset, pop_size=p, no_gens=g)
    gpc.run_backtest = 1
    pytest.gpc = gpc

@when(parsers.cfparse('run with evaluator "{evaluator:String}"',
                       extra_types=EXTRA_TYPES), target_fixture='evaluator')
@when('run with evaluator "<evaluator>"')
def gpc_with_set_evaluator(evaluator):
    pytest.gpc.set_test_evaluator(evaluator)
    pytest.gpc.run_gp()

@then('either max fitness improves over the generations')
def either_max_fitness_improves():
    pytest.f_max = pytest.gpc.gp.logbook.select("max")

@then('or min fitness improves over generations')
def or_min_fitness_improves(utils):
    pytest.f_min = pytest.gpc.gp.logbook.select("min")
    max_increases = utils.check_seq_increases(pytest.f_max)
    min_increases = utils.check_seq_increases(pytest.f_min)
    assert max_increases or min_increases
