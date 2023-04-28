import os
import os.path
from pytest_bdd import scenarios, given, when, then, parsers

from tests.fixtures import utils
from condorgp.params import lean_dict, test_dict, util_dict
from condorgp.evaluation.lean.lean_runner import RunLean

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

scenarios('../features/02_lean_algos.feature')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#             Lean tests each evolved individual
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
Scenario Outline: Lean tests each individual
    Given a Lean container ready to run
    And an evolved "<individual>" is specified
    When Lean runs the "<input_ind>" via the CLI
    Then the "<individual>" is used
    And the "<input_ind>" algorithm is tidied away
"""

'''
    # NB:
        These tests also confirm:
            that the fitness is found, and the log is up to date
'''

@given('a Lean container ready to run')
def lean_container_tested_already():
    pass # assumes local lean:latest image extant

@given(parsers.cfparse('an evolved "{input_ind:String}" is specified',
                       extra_types=EXTRA_TYPES), target_fixture='input_ind')
@given('an evolved "<input_ind>" is specified', target_fixture='input_ind')
def copy_config_n_algo_across(utils, input_ind):
    '''
    copies across config files and algorithms as needed
    '''
    utils.copy_config_in(input_ind)
    utils.copy_algo_in(input_ind)

@when(parsers.cfparse('Lean runs the "{input_ind:String}" via the CLI',
                       extra_types=EXTRA_TYPES), target_fixture='input_ind')
@when('Lean runs the "<input_ind>" via the CLI', target_fixture='input_ind')
def set_lean_runner(input_ind):
    '''uses the utils method to set an os system command via Lean CLI'''
    # TO DO: not DRY!
    config_to_run = ''
    if input_ind[-1] == '1':
        config_to_run = test_dict['CONDOR_TEST_CONFIG_FILE_1']
    elif input_ind[-1] == '2':
        config_to_run = test_dict['CONDOR_TEST_CONFIG_FILE_2']
    lean = RunLean()
    lean.run_lean_via_CLI(input_ind+'.py', config_to_run)

@then(parsers.cfparse('the "{output_ind:String}" is found',
                       extra_types=EXTRA_TYPES), target_fixture='output_ind')
@then('the "<output_ind>" is found', target_fixture='output_ind')
def results_files_are_updated(utils, output_ind):
    '''
    checks in the log file that the algo name is found
    only uses the last X lines of the log file
    '''
    assert utils.confirm_ind_name_in_log_lines(output_ind)

@then(parsers.cfparse('the result: "{ROI_over_MDD_value:Float}" is reported',
                       extra_types=EXTRA_TYPES), target_fixture='ROI_over_MDD_value')
@then('the result: "<ROI_over_MDD_value>" is reported', target_fixture='ROI_over_MDD_value')
def check_results(ROI_over_MDD_value, utils):
    key_req = 'Return Over Maximum Drawdown'
    limit_lines = 25 # util_dict['NO_LOG_LINES']
    got = utils.get_key_line_in_lim(key_req, limit_lines = limit_lines)

    assert got[0] != 'not found'
    assert got[1] > 0 and got[1] < limit_lines
    assert ROI_over_MDD_value == float(utils.get_last_chars(got[0]))

@then(parsers.cfparse('the "{input_ind:String}" algorithm is tidied away',
                       extra_types=EXTRA_TYPES), target_fixture='input_ind')
@then('the "<input_ind>" algorithm is tidied away')
def tidy_up_algorithms(utils, input_ind):
    '''
    deletes algorithms on path as found
    '''
    test_algos_path = lean_dict['LOCALPACKAGES_PATH']

    print(f"looking to delete:  {test_algos_path}{input_ind}.py")
    utils.delete_file_from_path(test_algos_path, input_ind+'.py')
    assert not os.path.exists(f"{test_algos_path}{input_ind}.py")
