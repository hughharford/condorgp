import os
import os.path

import logging

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

pytest.u = None
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
    Factory().start_logger()

    pytest.gpc = gpc

    gpc.use_adfs = 1
    pset_used = pset # 'test_adf_symbreg_pset' - see .feature

    p = 15
    g = 30
    cp_base = "test_08_fitmax"
    cp_freq = g+1
    gpc.set_gp_n_cp(freq=cp_freq, cp_file=cp_base+"")
    gpc.setup_gp(pset_spec=pset_used, pop_size=p, no_gens=g)

    gpc.run_backtest = 0
    gpc.inject_strategy = 0 # set to 1, this selects naut_06_gp_strategy

@when(parsers.cfparse('run with evaluator "{evaluator:String}"',
                       extra_types=EXTRA_TYPES), target_fixture='evaluator')
@when('run with evaluator "<evaluator>"')
def gpc_with_set_evaluator(evaluator):
    eval_used = 'evalSymbRegTest' # - see .feature
    pytest.gpc.set_test_evaluator(evaluator)
    pytest.gpc.run_gp()

@then('max fitness is static or improves over generations')
def either_max_fitness_improves(utils):

    logging.info(' deap __ Logbook __ via: test_08_fitmax_done')
    logging.info(pytest.gpc.gp.logbook)

    pytest.f_max = pytest.gpc.gp.logbook.select("max")
    max_never_decrs = utils.check_seq_never_decreases(pytest.f_max)
    assert (max_never_decrs)
    assert pytest.f_max[-1] > pytest.f_max[0]

    pytest.u = utils

    # tidy up
def teardown_module():
    pass
    # pytest.u.tidy_cp_files(pytest.cp_base)
