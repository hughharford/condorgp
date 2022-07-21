import os

from pytest_bdd import scenarios, given, when, then, parsers

from condorgp.utils import get_last_x_log_lines
from condorgp.utils import copy_config_json_to_lean_launcher_dir
from condorgp.utils import copy_ind_to_lean_algos_dir
from condorgp.params import lean_dict, test_dict, util_dict

from condorgp.lean_runner import RunLean

EXTRA_TYPES = {
    'Number': int,
    'String': str,
}

CONVERTERS = {
    'initial': int,
    'some': int,
    'total': int,
}

scenarios('../features/03_lean_test_individual.feature')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#             Lean tests each evolved individual
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
Scenario Outline: Lean tests each individual
    Given a Lean container ready to run
    And an evolved "<individual>" is specified
    When Lean runs
    Then the "<individual>" is used
"""

# LEAN_ALGOS_FOLDER
# copy_ind_to_lean_algos_dir

@given('a Lean container ready to run')
def lean_container_tested_already():
    pass # assumes local lean:latest image extant

@given(parsers.cfparse('an evolved "{input_ind:String}" is specified',
                       extra_types=EXTRA_TYPES), target_fixture='input_ind')
@given('an evolved "<input_ind>" is specified', target_fixture='input_ind')
def copy_config_n_algo_across(input_ind):
    # copy config.json across before container launch
    config_to_copy = test_dict['CONDOR_TEST_CONFIG_FILE']
    config_path = test_dict['CONDOR_CONFIG_PATH']
    copy_config_json_to_lean_launcher_dir(config_path, config_to_copy)

    # copy algo.py across before container launch
    test_ind_path = test_dict['CONDOR_TEST_ALGOS_FOLDER']
    copy_ind_to_lean_algos_dir(test_ind_path, input_ind + '.py')


@when('Lean runs')
def set_lean_runner():
    '''uses the utils method to set an os system command via Lean CLI'''
    lean = RunLean()
    lean.run_lean_via_CLI()

@then(parsers.cfparse('the "{output_ind:String}" is found',
                       extra_types=EXTRA_TYPES), target_fixture='output_ind')
@then('the "<output_ind>" is found', target_fixture='output_ind')
def results_files_are_updated(output_ind):
    results_path = lean_dict['LEAN_RESULTS_FOLDER']
    output_ind_with_path = results_path + output_ind
    print(output_ind)
    no_lines = util_dict['NO_LOG_LINES']
    results_list = get_last_x_log_lines(lines = no_lines, log_file_n_path = lean_dict['BACKTEST_LOG_FILE_N_PATH'])
    found_algo_name = False
    for line in results_list:
        if output_ind in line:
            print(line)
            found_algo_name = True
    assert found_algo_name
