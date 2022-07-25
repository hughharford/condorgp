import os
import sys
from os.path import exists

from pytest_bdd import scenarios, given, when, then, parsers

from condorgp.lean_runner import RunLean
from condorgp.utils import retrieve_log_line_with_key
from condorgp.utils import get_keyed_line_within_limits
from condorgp.params import lean_dict, test_dict

EXTRA_TYPES = {
    'Number': int,
    'String': str,
    'Float': float
}

CONVERTERS = {
    'initial': int,
    'some': int,
    'total': int,
}

scenarios('../features/05_lean_inject_algo.feature')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#             Lean reports results for each evolved individual
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
  Scenario Outline: Lean reports results for injected individual
    Given a Lean container ready to run
    And a Lean algo wrapper that works
    And a text of "<evolved_code>" is injected from a file
    When Lean runs the "<input_ind>" via the CLI
    Then the result: "<Return_Over_Maximum_Drawdown>" is reported
    And the fitness function demonstrates this result

    Examples:
      | evolved_code        | input_ind       | Return_Over_Maximum_Drawdown  |
      | file_with_gp_code   | gpInjectAlgo1   | 999999                        |
"""

WORKING_ALGO_WRAPPER_FILE = lean_dict['WORKING_ALGO_WRAPPER_FILE']

@given('a Lean container ready to run')
def docker_image_exists():
    '''
    N.B >> duplicate requirement as test_04

    Should check the docker images (locally / then cloud).
    For now: assumes local lean:latest image extant
    TODO: Actually implement this

    current docker image: quantconnect/lean:latest

    '''
    pass

@given('a Lean algo wrapper that works')
def working_algo_wrapper():
    assert WORKING_ALGO_WRAPPER_FILE # i.e. is not empty

#  And a text of "<evolved_code>" is injected
@given(parsers.cfparse('a text of "{evolved_code:String}" is injected',
                       extra_types=EXTRA_TYPES), target_fixture='evolved_code')
@given('a text of "<evolved_code>" is injected', target_fixture='evolved_code')
def individual_specified(evolved_code):
    '''
    An algorithm 'individual' is specified based on evolved_code variable
    Confirms this is present, length > 0
    '''
    assert len(evolved_code) > 0

@when(parsers.cfparse('Lean runs the "{input_ind:String}" via the CLI',
                       extra_types=EXTRA_TYPES), target_fixture='input_ind')
@when('Lean runs the "<input_ind>" via the CLI', target_fixture='input_ind')
def runs_the_individual_via_the_cli(input_ind):
    '''
    Calls the CLI runner class, with the algorithm specified
    '''
    pass
    # r = RunLean()
    # r.run_lean_via_CLI(input_ind)

@then(parsers.cfparse('the result: "{Return_Over_Maximum_Drawdown:Float}" is reported',
                       extra_types=EXTRA_TYPES), target_fixture='Return_Over_Maximum_Drawdown')
@then('the result: "<Return_Over_Maximum_Drawdown>" is reported', target_fixture='Return_Over_Maximum_Drawdown')
def expected_result_is_updated(Return_Over_Maximum_Drawdown):
    '''
    Checks the expected result

    With different specific algorithms, different results expected
    Currently using
        lean_dict['FITNESS_CRITERIA']
        22 07: Return_Over_Maximum_Drawdown
    '''
    key_req = Return_Over_Maximum_Drawdown
    limit_lines = 50
    got = get_keyed_line_within_limits(key_req, limit_lines = limit_lines)
    assert got[0] != ''
    assert got[1] < limit_lines

@then('the fitness function demonstrates this result')
def fitness_function_demos_the_result():
    '''
    The fitness function gathers the result
    '''
    pass
