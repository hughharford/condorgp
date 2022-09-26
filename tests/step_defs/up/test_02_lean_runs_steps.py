import os
import sys
from os.path import exists

import pytest
from pytest_bdd import scenarios, given, when, then, parsers

from condorgp.lean_runner import RunLean
from condorgp.utils import Utils

from condorgp.params import lean_dict, test_dict, util_dict

EXTRA_TYPES = {
    'Number': int,
    'String': str,
}

CONVERTERS = {
    'initial': int,
    'some': int,
    'total': int,
}

scenarios('../../features/02_lean_runs.feature')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#             Lean runs and outputs results
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
Scenario: Basic Lean run
    Given quantconnect/lean:latest docker image
    And lean_runner py file with RunLean class and run_lean_via_CLI method
    When RunLean.run_lean_via_CLI is run
    Then Lean/Backtests files are updated
"""

class UtilTest:
    def __init__(self) -> None:
        self.u = Utils()

@pytest.fixture
def utils():
    util = UtilTest()
    return util.u

@given('quantconnect/lean:latest docker image')
def docker_image_exists():
    '''
    Should check the docker images (locally / then cloud).
    For now: assumes local lean:latest image extant
    TODO: implement this
    '''
    pass

@given('lean_runner py file with RunLean class and run_lean_via_CLI method')
def confirms_class_and_method_exist():
    '''
    Intended to confirm (1) the class file, and:
        confirm class name exists (2)
        confirm method name exists (3)
    Hard coded for now
    '''
    full_local_path = '/home/hsth/code/hughharford/condorgp/condorgp/'
    py_file_required = 'lean_runner.py'
    class_required = 'RunLean'
    method_required = 'run_lean_via_CLI'
    file_to_open = full_local_path + py_file_required
    assert os.path.exists(file_to_open)

    class_found = False
    method_found = False
    with open(file_to_open)as class_file:
        lines = class_file.readlines()
        for line in lines:
            if class_required in line: class_found = True
            if method_required in line: method_found = True

    assert class_found
    assert method_found


@when('RunLean.run_lean_via_CLI is run')
def call_run_docker():
    '''
    Calls the CLI runner class once
    '''
    # input_ind = test_dict['BASIC_TEST_ALGO_NAME']
    # config_to_run = test_dict['CONFIG_TEST_ALGOS_FILE_1']
    # lean = RunLean()
    # lean.run_lean_via_CLI() # input_ind, config_to_run)
    pass
    # DROPPED this as time consuming, and test_03 covers same ground

@then('Lean/Backtests files are updated')
def results_files_are_updated():
    '''
    Lean/Backtests result files are
        (1) there, i.e. >1 file
        (2) updated within reasonable timeframe
    '''
    pass
    # SEE COMMENT IN METHOD ABOVE

    # results_file = lean_dict['BACKTEST_LOG_LOCALPACKAGES']
    # log_found = get_last_x_log_lines(
    #                                 lines = util_dict['NO_LOG_LINES'],
    #                                 log_file_n_path = results_file)
    # output = []
    # for line in log_found:
    #     output.append(line)

    # assert len(output) >= 10
    # assert check_recent_mod(test_dict['CONDORGP_IN_BACKTESTS_DIR'])
