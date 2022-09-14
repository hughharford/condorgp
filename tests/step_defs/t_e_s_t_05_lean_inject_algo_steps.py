import os
import sys
from os.path import exists

from pytest_bdd import scenarios, given, when, then, parsers

from condorgp.lean_runner import RunLean
from condorgp.utils import retrieve_log_line_with_key
from condorgp.utils import get_keyed_line_within_limits
from condorgp.utils import get_all_lines
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
    And a text of "<gp_code_file>" is injected from a file
    When Lean runs the "<input_ind>" via the CLI
    Then the result: "<Return_Over_Maximum_Drawdown>" is reported
    And the fitness function demonstrates this result

    Examples:
      | gp_code_file        | input_ind       | Return_Over_Maximum_Drawdown  |
      | file_with_gp_code   | gpInjectAlgo1   | 999999                        |
"""

ALGO_WRAPPER_SIN_PY = lean_dict['ALGO_WRAPPER_SIN_PY']

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
    assert ALGO_WRAPPER_SIN_PY # i.e. is not empty
    file_exists = test_dict['CONDOR_CONFIG_PATH'] + ALGO_WRAPPER_SIN_PY + '.py'
    print(file_exists)
    assert os.path.isfile(file_exists)

#  And a text of "<gp_code_file>" is injected
@given(parsers.cfparse('a text of "{gp_code_file:String}" is injected',
                       extra_types=EXTRA_TYPES), target_fixture='gp_code_file')
@given('a text of "<gp_code_file>" is injected', target_fixture='gp_code_file')
def individual_specified(gp_code_file):
    '''
    An algorithm 'individual' is specified based on gp_code_file variable
    Confirms this is present, length > 0
    '''
    ROOT = '/home/hsth/code/hughharford/condorgp/condorgp/gp/output/'
    f_path = ROOT + gp_code_file
    lines = get_all_lines(f_path)
    assert len(lines) > 0

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
    pass
    # get from updated test_04
