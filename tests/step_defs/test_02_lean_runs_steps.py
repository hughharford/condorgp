import os
import sys
from os.path import exists

from pytest_bdd import scenarios, given, when, then, parsers

from condorgp.lean_runner import RunLean
from condorgp.utils import check_recent_mod
from condorgp.params import lean_dict, test_dict

EXTRA_TYPES = {
    'Number': int,
    'String': str,
}

CONVERTERS = {
    'initial': int,
    'some': int,
    'total': int,
}

scenarios('../features/02_lean_runs.feature')

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

@given('quantconnect/lean:latest docker image')
def docker_image_exists():
    '''
    Should check the docker images (locally / then cloud).
    For now: assumes local lean:latest image extant
    TODO: Actually implement this
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
    path_to_check = 'condorgp/'
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
    input_ind = test_dict['BASIC_TEST_ALGO_NAME']
    config_to_run = test_dict['CONFIG_TEST_ALGOS_FILE_1']
    lean = RunLean()
    lean.run_lean_via_CLI(input_ind, config_to_run)

@then('Lean/Backtests files are updated')
def results_files_are_updated():
    '''
    Lean/Backtests result files are
        (1) there, i.e. >1 file
        (2) updated within reasonable timeframe
    '''
    # results_path = lean_dict['LEAN_BACKTEST_OUTPUTS_DIR']
    # results_files = [results_path + x for
    #                  x in os.listdir(results_path)
    #                  if os.path.isfile(results_path + x)]
    results_file = lean_dict['BACKTEST_LOG_LOCALPACKAGES']
    results_files = []
    results_files.append(results_file)
    assert len(results_files) >= 1
    assert check_recent_mod(results_files)
