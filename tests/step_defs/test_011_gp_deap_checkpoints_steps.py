import os
import os.path
import time
import glob

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

pytest.checkpointfile = ""
pytest.cp_path = ""
pytest.given_cp_file = ""

scenarios('../features/011_gp_deap_checkpoints.feature')

"""
Feature: GpControl's evolution improves fitness over time
  As a gp algorithm, considerable time is taken evolved code
  This means checkpointing and restarting are essential,
  To ensure restarting from zero isn't needed every time.

  Scenario Outline: Evolved populations can be checkpointed
    Given gp_deap_adf.GpDeapAdfCp
    When a 6 generation run with checkpoints every 3 is made
    Then the checkpoint file is created at generation 3
    And the checkpoint is updated at generation 6
"""
@given('gp_deap_adf.GpDeapAdfCp')
def ability_to_checkpoint(gpc):
    gpc.verbose = 0
    gpc.use_adfs = 1
    pset_used = 'naut_pset_02_adf'
    p = 2
    g = 7
    cp_freq = 3

    gpc.set_gp_n_cp(freq=cp_freq, cp_file="test_011_6g_2cps__")
    gpc.setup_gp(pset_spec=pset_used, pop_size=p, no_gens=g)
    gpc.run_backtest = 0

@when('a 6 generation run with checkpoints every 3 is made')
def six_gen_run_with_cps_every_three(gpc):
    eval_used = 'eval_nautilus'
    gpc.set_test_evaluator(eval_used)
    gpc.run_gp()

@then('the checkpoint file is created at generation 3')
def first_new_checkpoint_file_created(gpc, params):
    now = time.time()
    pytest.given_cp_file = gpc.gp.checkpointfile
    pytest.cp_path = params.naut_dict['CHECKPOINT_PATH']
    cp_path = pytest.cp_path + \
        pytest.given_cp_file.split('.')[0] + '_3.pkl'
    pytest.checkpointfile = pytest.given_cp_file
    assert os.path.isfile(cp_path)
    # get time of creation
    ti_c = os.path.getctime(cp_path)
    assert (now - ti_c) < 60

@then('the checkpoint is updated at generation 6')
def second_new_checkpoint_file_created(gpc, params):
    now = time.time()
    cp_path = pytest.cp_path + \
        pytest.given_cp_file.split('.')[0] + '_6.pkl'
    assert os.path.isfile(cp_path)
    # get last time of modification
    ti_m = os.path.getmtime(cp_path)
    assert (now - ti_m) < 60

    # tidy up
def teardown_module(gpc):
    p = pytest.cp_path
    f = pytest.given_cp_file.split('.')[0]
    for filename in glob.glob(f"{p}{f}*"):
        os.remove(filename)
        assert not os.path.isfile(filename)
