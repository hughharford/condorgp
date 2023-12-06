import os
import os.path

import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from tests.fixtures import *
from condorgp.params import Params

pytest.DEAP_ONE = ""

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

scenarios('../features/05a_gp_find_fitness.feature')

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
      | naut_02_egFX.py | naut-run-02 | 15.966514528587545  |
      | naut_03_egFX.py | naut-run-03 | -21.49663142709111  |
      | naut_04_egFX.py | naut-run-04 | -16.160361991815254 |
    # SHOULD SWITCH THESE TO MAKE IT MORE DIFFICULT


  Scenario Outline: find_fitness finds the latest fitness from logs
    Given the test_find_fitness_2.json
    When find_fitness gets the latest fitness for "<naut_runner>"
    And checks the runner name is "<runner_name>"
    Then the latest fitness found is "<sharpe_ratio>"
    # i.e. doesn't get confused by earlier naut-run-04 entries x 2
    # or other naut-run-02 entries with different earlier outputs x2

    Examples:
      | naut_runner     | runner_name | sharpe_ratio       |
      | naut_02_egFX.py | naut-run-02 | 15.966514528587545 |
      | naut_03_egFX.py | naut-run-03 | -21.49663142709111 |
"""

@given('the test_find_fitness_1.json')
def check_json_in_test_data_1():
    pass # assumes, rest of test to prove

@when(parsers.cfparse('find_fitness gets fitness for "{naut_runner:String}"',
      extra_types=EXTRA_TYPES), target_fixture='naut_runner')
@when('find_fitness gets fitness for "<naut_runner>"',
      target_fixture='naut_runner')
def nautilus_runner_1(naut_runner):
    ''' purely for reference '''
    pass # it's the runner_name that is searched

# runner_name
@when(parsers.cfparse('and the runner name is "{runner_name:String}"',
      extra_types=EXTRA_TYPES), target_fixture='runner_name')
@when('and the runner name is "<runner_name>"',
      target_fixture='runner_name')
def runner_name_1(runner_name):
    ''' criteria for which runner's output to search for '''
    pass # it's the runner_name that is searched

@then(parsers.cfparse('the fitness found is "{sharpe_ratio:String}"',
                      extra_types=EXTRA_TYPES), target_fixture='sharpe_ratio')
@then('the pset returns contains "<sharpe_ratio>"')
def fitness_found_is_1(sharpe_ratio):
    pass
