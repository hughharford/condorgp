import os
import os.path
import time

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
pytest.checkpointfilepath = ""

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
    p = 1
    g = 1
    gpc.use_adfs = 1
    gpc.select_gp_provider()
    gpc.setup_gp(pset_spec="naut_pset_02_adf", pop_size=p, no_gens=g)
    gpc.run_backtest = 0
    gpc.checkpointfile = "test_011_6g_2cps__"
    pytest.gpc = gpc

@when('a 6 generation run with checkpoints every 3 is made')
def six_gen_run_with_cps_every_three():
    pytest.gpc.set_test_evaluator("eval_nautilus")
    pytest.gpc.run_gp()

@then('the checkpoint file is created at generation 3')
def new_checkpoint_file_created(gpc, params):
    now = time.time()
    cp_path = params.naut_dict['CHECKPOINT_PATH'] + gpc.checkpointfile +'.pkl'
    pytest.checkpointfilepath = cp_path
    assert os.path.isfile(cp_path)
    # get time of creation
    ti_c = os.path.getctime(cp_path)
    assert (now - ti_c) < 60

    # Converting the time in seconds to a timestamp
    # c_ti = time.ctime(ti_c)
    # m_ti = time.ctime(ti_m)

@then('the checkpoint is updated at generation 6')
def new_checkpoint_file_created(gpc, params):
    now = time.time()
    cp_path = pytest.checkpointfilepath
    assert os.path.isfile(cp_path)
    # get last time of modification
    ti_m = os.path.getmtime(cp_path)
    assert (now - ti_m) < 60

    # tidy up
def teardown_module():
    cp_path = pytest.checkpointfilepath
    os.remove(cp_path)
    assert not os.path.isfile(cp_path)
