import os.path
from pytest_bdd import scenarios, given, when, then, parsers
import logging
import pytest

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

pytest.OUTPUT_IND = ""

scenarios('../../features/up/02_nautilus_algos.feature')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#             Nautilus tests each evolved individual
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

'''
Feature: Nautilus tests each evolved individual
  As a fitness function,
  I want to Nautilus to run each fitness test,
  So that I can get a fitness score for each.

  Scenario Outline: Nautilus tests each individual
    Given a Nautilus setup ready to run
    And an evolved "<input_ind>" is specified
    When Nautilus runs the "<input_ind>"
    Then the "<output_ind>" is found
    And the result: "<expected_value>" is reported

    Examples:
      | input_ind        |   output_ind   |   expected_value      |
      | naut_03_egFX.py  |   naut-run-03  |   -21.49663142709111  |
      | naut_04_egFX.py  |   naut-run-04  |   -16.160361991815254 |

'''

@given('a Nautilus setup ready to run')
def nautilus_setup_is_ready():
    pass # assumption for now: working as of 23 11 15

@given(parsers.cfparse('an evolved "{input_ind:String}" is specified',
                       extra_types=EXTRA_TYPES), target_fixture='input_ind')
@given('an evolved "<input_ind>" is specified', target_fixture='input_ind')
def input_evolved_code(input_ind):
    '''
        not operational for now
    '''
    pass # not required, as can now run from:
         # condorgp/evaluation/nautilus using run_naut.py


@when(parsers.cfparse('Nautilus runs the "{input_ind:String}"',
                       extra_types=EXTRA_TYPES), target_fixture='input_ind')
@when('Nautilus runs the "<input_ind>"', target_fixture='input_ind')
def run_nautilus_and_evaluator(input_ind, initial_factory):
    ''' runs nautilus as per the required evaluator etc'''
    script_to_run = input_ind
    nt = initial_factory.get_backtest_runner()
    logging.info("test_02 >> Running RunNautilus")
    nt.basic_run(specified_script=script_to_run)

@then(parsers.cfparse('the "{output_ind:String}" is found',
                       extra_types=EXTRA_TYPES), target_fixture='output_ind')
@then('the "<output_ind>" is found', target_fixture='output_ind')
def results_files_are_updated(output_ind):
    '''
    checks in the log file that the algo name is found
    only uses the last X lines of the log file
    '''
    assert output_ind
    pytest.OUTPUT_IND = output_ind

@then(parsers.cfparse('the result: "{expected_value:Float}" is reported',
                    extra_types=EXTRA_TYPES),
                    target_fixture='expected_value')
@then('the result: "<expected_value>" is reported',
                    target_fixture='expected_value')
def check_results(expected_value, utils, params):
    key_req = params.naut_dict['FITNESS_CRITERIA']
    logging.info(key_req)
    backtest_id = pytest.OUTPUT_IND
    lines = 10000
    max_lines_diff = 300 #

    got2 = utils.find_fitness_with_matching_backtest(
            key = key_req,
            log_file_n_path = "",
            backtest_id = backtest_id,
            lines = lines,
            max_lines_diff = max_lines_diff)

    assert got2[1] != -1
    found_fitness = ""
    if got2[1] != -1:
        found_fitness = float(utils.get_last_chars(got2[0],2))
    assert found_fitness == expected_value
