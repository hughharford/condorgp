import os
import os.path

import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from condorgp.gp.gp_functions import GpFunctions
from condorgp.params import Params

pytest.p = Params()
pytest.r_name_1 = ""
pytest.r_name_2 = ""
pytest.log1 = ""
pytest.log2 = ""

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

scenarios('../../features/up/06_gp_find_fitness.feature')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#             find_fitness correctly return fitness
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
Feature: Finding the fitness after every test is critcal
  As part of a gp system,
  gp_functions.find_fitness needs to correct find fitness from logs,
  To ensure evolution is effective.

  Scenario Outline: find_fitness can correctly find fitness from logs
    Given the test_find_fitness_1.json
    When find_fitness gets fitness for "<naut_runner>"
    And the runner name is "<runner_name>"
    Then the fitness found is "<sharpe_ratio>"

    Examples:
      | naut_runner     | runner_name | sharpe_ratio        |
      | naut_04_egFX.py | naut-run-04 | -16.160361991815254 |
      | naut_03_egFX.py | naut-run-03 | -21.49663142709111  |
      | naut_02_egFX.py | naut-run-02 | 15.966514528587545  |
      | fictional.py    | naut-run-77 | -111000             |

"""
# SCENARIO 1
# ===============================================================
@given('the test_find_fitness_1.json')
def check_json_in_test_data_1(utils, params):
    ''' confirms test json log in place '''
    json_path = pytest.p.test_dict["CGP_TEST_DATA"]+"test_find_fitness_1.json"
    false_json_path = pytest.p.test_dict["CGP_TEST_DATA"]+"test_find_fitness_3.json"
    assert utils.confirm_file_extant(json_path)
    assert not utils.confirm_file_extant(false_json_path)
    pytest.log1 = json_path

@when(parsers.cfparse('find_fitness gets fitness for "{naut_runner:String}"',
      extra_types=EXTRA_TYPES), target_fixture='naut_runner')
@when('find_fitness gets fitness for "<naut_runner>"',
      target_fixture='naut_runner')
def nautilus_runner_1(naut_runner):
    ''' purely for reference '''
    pass # it's the runner_name that is searched

@when(parsers.cfparse('the runner name is "{runner_name:String}"',
extra_types=EXTRA_TYPES), target_fixture='runner_name')
@when('the runner name is "<runner_name>"',
      target_fixture='runner_name')
def runner_name_1(runner_name):
    ''' criteria for which runner's output to search for '''
    # it's the runner_name that is searched
    pytest.r_name_1 = runner_name

@then(parsers.cfparse('the fitness found is "{sharpe_ratio:String}"',
                      extra_types=EXTRA_TYPES), target_fixture='sharpe_ratio')
@then('the fitness found is "<sharpe_ratio>"')
def fitness_found_is_1(gpf, sharpe_ratio):
    ''' check sharpe's ratio reported is as expected '''
    assert float(sharpe_ratio) == gpf.find_fitness(backtest_id=pytest.r_name_1,
                                                   log_file_n_path=pytest.log1)


# SCENARIO 2
# ===============================================================
'''
Scenario Outline: find_fitness finds the latest fitness from logs
    Given the test_find_fitness_2.json
    When find_fitness gets the latest fitness for "<naut_runner>"
    And checks the runner name is "<runner_name>"
    Then the latest fitness found is "<sharpe_ratio>"
    # i.e. doesn't get confused by earlier naut-run-04 entries x 2
    # or other naut-run-02 entries with different earlier output3 x2

    Examples:
      | naut_runner     | runner_name | sharpe_ratio       |
      | naut_02_egFX.py | naut-run-02 | 15.966514528587545 |
      | naut_03_egFX.py | naut-run-03 | -21.49663142709111 |
'''

@given('the test_find_fitness_2.json')
def check_json_in_test_data_2(utils):
    ''' confirms test json log in place '''
    json_path = pytest.p.test_dict["CGP_TEST_DATA"]+"test_find_fitness_2.json"
    assert utils.confirm_file_extant(json_path)
    pytest.log2 = json_path

@when(parsers.cfparse('find_fitness gets the latest fitness for "{naut_runner:String}"',
      extra_types=EXTRA_TYPES), target_fixture='naut_runner')
@when('find_fitness gets the latest fitness for "<naut_runner>"',
      target_fixture='naut_runner')
def nautilus_runner_2(naut_runner):
    ''' purely for reference '''
    pass # it's the runner_name that is searched


@when(parsers.cfparse('checks the runner name is "{runner_name:String}"',
      extra_types=EXTRA_TYPES), target_fixture='runner_nam=e')
@when('checks the runner name is "<runner_name>"',
      target_fixture='runner_name')
def runner_name_2(runner_name):
    ''' criteria for which runner's output to search for '''
    # it's the runner_name that is searched
    pytest.r_name_2 = runner_name

@then(parsers.cfparse('the latest fitness found is "{sharpe_ratio:String}"',
                      extra_types=EXTRA_TYPES), target_fixture='sharpe_ratio')
@then('the latest fitness found is "<sharpe_ratio>"')
def fitness_found_is_2(gpf, sharpe_ratio):
    ''' check sharpe's ratio reported is as expected '''
    assert float(sharpe_ratio) == gpf.find_fitness(backtest_id=pytest.r_name_2,
                                                   log_file_n_path=pytest.log2)
