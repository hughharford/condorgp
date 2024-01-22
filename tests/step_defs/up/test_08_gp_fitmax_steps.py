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

    eval_used = 'eval_nautilus'
    pset_used = 'naut_pset_02_adf' #  'test_pset5b'
    gpc.run_backtest = 0

    p = 2
    g = 7 # this accumulates, provided _done included in cp_file
    cp_freq = 3
    gpc.use_adfs = 1

    gpc.set_gp_n_cp(freq=cp_freq, cp_file="test_08_fitmax_done")
    gpc.setup_gp(pset_spec=pset_used, pop_size=p, no_gens=g)
    gpc.set_test_evaluator(eval_used)

    pytest.gpc = gpc

@when(parsers.cfparse('run with evaluator "{evaluator:String}"',
                       extra_types=EXTRA_TYPES), target_fixture='evaluator')
@when('run with evaluator "<evaluator>"')
def gpc_with_set_evaluator(evaluator):
    pytest.gpc.set_test_evaluator(evaluator)
    pytest.gpc.run_gp()

@then('max fitness is static or improves over generations')
def either_max_fitness_improves(utils):

    logging.info(' deap __ Logbook __ via: test_08_fitmax_done')
    logging.info(pytest.gpc.gp.logbook)

    pytest.f_max = pytest.gpc.gp.logbook.select("max")
    max_incrs = utils.check_seq_increases(pytest.f_max)
    max_never_decrs = utils.check_seq_never_decreases(pytest.f_max)
    assert (max_incrs or max_never_decrs)
    # assert max_incrs

    pytest.u = utils
    # tidy up
def teardown_module():
    chpt_path = pytest.u.p.naut_dict['CHECKPOINT_PATH']
    import glob
    # All files and directories ending with .txt and that don't begin with a dot:
    to_delete = glob.glob(f"{chpt_path}test_08_fitmax_*.pkl")
    to_delete.sort()
    for f in range(len(to_delete)-2):
        if to_delete[f] != chpt_path+'test_08_fitmax_done.pkl':
            pass
            os.remove(to_delete[f])
