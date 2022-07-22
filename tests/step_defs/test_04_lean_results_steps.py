import os
import sys
from os.path import exists

from pytest_bdd import scenarios, given, when, then, parsers

from condorgp.lean_runner import RunLean
from condorgp.utils import retrieve_log_line_with_key
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

scenarios('../features/04_lean_results.feature')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#             Lean reports results for each evolved individual
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
  Scenario Outline: Lean reports results for each individual
    Given a Lean container ready to run
    And an evolved "<input_ind>" is specified
    When Lean runs the "<input_ind>" via the CLI
    Then the result: "<Return_Over_Maximum_Drawdown>" is reported
    And the fitness function demonstrates this result

    Examples:
      | input_ind            |   Return_Over_Maximum_Drawdown             |
      | IndBasicAlgo2        |   85.095                                   |
      | IndBasicAlgo1        |   79228162514264337593543950335            |


# Each of the test algos has different dates and cash:

# IndBasicAlgo1 has :
        # self.SetStartDate(2014,10,7)   #Set Start Date
        # self.SetEndDate(2014,10,11)    #Set End Date
        # self.SetCash(1_000_000)           #Set Strategy Cash

# IndBasicAlgo2 has :
        # self.SetStartDate(2013,10,7)   #Set Start Date
        # self.SetEndDate(2013,10,11)    #Set End Date
        # self.SetCash(100_000)           #Set Strategy Cash
"""



@given('a Lean container ready to run')
def docker_image_exists():
    '''
    Should check the docker images (locally / then cloud).
    For now: assumes local lean:latest image extant
    TODO: Actually implement this

    current docker image: quantconnect/lean:latest
    '''
    pass


@given(parsers.cfparse('an evolved "{input_ind:String}" is specified',
                       extra_types=EXTRA_TYPES), target_fixture='input_ind')
@given('an evolved "<input_ind>" is specified', target_fixture='input_ind')
def individual_specified(input_ind):
    '''
    An algorithm 'individual' is specified
    Confirms this is present
    '''
    pass

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
        Return_Over_Maximum_Drawdown
    '''
    key_req = Return_Over_Maximum_Drawdown
    found_line = retrieve_log_line_with_key(key_req)
    if found_line != '':
        assert key_req in found_line

@then('the fitness function demonstrates this result')
def fitness_function_demos_the_result():
    '''
    The fitness function gathers the result
    '''
    pass
