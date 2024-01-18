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

scenarios('../../features/up/08_gp_fitmax.feature')

"""
  Scenario Outline: Evolved code shows fitness improvement
    Given GpControl is run with "<pset>"
    When run with evaluator "<evaluator>"
    Then max fitness is static or improves over generations

  Examples:
    |  pset         |   evaluator          |
    |  naut_pset_01 |   eval_nautilus      |
"""

@given(parsers.cfparse('GpControl is run with "{pset:String}"',
                       extra_types=EXTRA_TYPES), target_fixture='pset')
@given('GpControl is run with "<pset>"')
def gpcontrol_run_001(gpc, pset):
    p = 2
    g = 3
    cp_freq = 0
    gpc.set_gp_n_cp(freq=cp_freq, cp_file="empty")
    gpc.setup_gp(pset_spec=pset, pop_size=p, no_gens=g)
    gpc.run_backtest = 1
    pytest.gpc = gpc

@when(parsers.cfparse('run with evaluator "{evaluator:String}"',
                       extra_types=EXTRA_TYPES), target_fixture='evaluator')
@when('run with evaluator "<evaluator>"')
def gpc_with_set_evaluator(evaluator):
    pytest.gpc.set_test_evaluator(evaluator)
    pytest.gpc.run_gp()

@then('max fitness is static or improves over generations')
def either_max_fitness_improves(utils):
    pytest.f_max = pytest.gpc.gp.logbook.select("max")
    max_incrs = utils.check_seq_increases(pytest.f_max)
    # max_never_decrs = utils.check_seq_never_decreases(pytest.f_max)
    # assert (max_incrs or max_never_decrs)
    assert max_incrs
