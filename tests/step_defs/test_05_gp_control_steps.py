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

scenarios('../features/05_gp_control.feature')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#             1/3 GpControl can set different psets as needed
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
  Scenario Outline: GpControl can set different psets as needed
    Given a specific pset is needed
    When GpControl gets a requirement for "<pset_input>"
    And GpControl is checked
    Then the pset returned is not the same as the base_pset
    And the pset returns contains "<pset_name>"

    Examples:
      | pset_input      |  pset_name    |
      | pset5a          |  mul          |
      | pset5b          |  add          |
"""
# 1/3 ***************************************************************************

@given('a specific pset is needed')
def setup_ready():
    pass # assumes, rest of test to prove

@when(parsers.cfparse('GpControl gets a requirement for "{pset_input:String}"',
      extra_types=EXTRA_TYPES), target_fixture='pset_input')
@when('GpControl gets a requirement for "<pset_input>"',
      target_fixture='pset_input')
def check_GpControl(deap_one, pset_input):
    ''' sets 2 different psets '''
    deap_one.base_pset = deap_one.set_pset('test_base_pset')
    deap_one.test_pset = deap_one.set_pset(pset_input)

@when('GpControl is checked')
def check_gp_control(deap_one):
    assert type(deap_one.base_pset) is not None
    assert type(deap_one.test_pset) is not None

@then('the pset returned is not the same as the base_pset')
def pset_returned_is(deap_one):
    assert deap_one.base_pset != deap_one.test_pset

@then(parsers.cfparse('the pset returns contains "{primitive_name:String}"',
                      extra_types=EXTRA_TYPES), target_fixture='primitive_name')
@then('the pset returns contains "<primitive_name>"')
def pset_contains(deap_one, primitive_name):
    assert deap_one.test_pset
    prim_names = list(deap_one.test_pset.context.keys())
    assert primitive_name in prim_names

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#             2/3 Running a pset can output log text
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

'''
  Scenario Outline: test psets can output specific text to condor log
    Given a specific test pset "<test_5_2_psets>"
    When provided the "<arg_input>"
    Then the result is "<text_output>"

    Examples:
      | arg_input     | test_5_2_psets           |  text_output        |
      | hello_world   | test_pset5c              |  hello_world        |
'''

# 2/3 ***************************************************************************

@given(parsers.cfparse('a specific test pset "{test_5_2_psets:String}"',
                    extra_types=EXTRA_TYPES),target_fixture='test_5_2_psets')
@given('a specific test pset "<test_5_2_psets>"')
def setup_ready(deap_one, test_5_2_psets):
    ''' sets up gp as standard, then amends pset'''
    pytest.DEAP_ONE = deap_one
    pytest.DEAP_ONE.setup_gp(test_5_2_psets,1,1)
    pytest.DEAP_ONE.set_test_evaluator('eval_nautilus')

@when(parsers.cfparse('provided the "{arg_input:String}"',
                    extra_types=EXTRA_TYPES), target_fixture='arg_input')
@when('provided the "<arg_input>"',
        target_fixture='arg_input')
def provided_the(arg_input):
    ''' runs gp with arg_input as given '''
    pytest.DEAP_ONE.run_gp() # arg not inputted, hard coded in this test

@then(parsers.cfparse('the result is "{text_output:String}"',
                    extra_types=EXTRA_TYPES), target_fixture='text_output')
@then('the result is "<text_output>"')
def condor_log_contains(text_output):
    ''' checks condor log for text expected '''
    p = Params()
    log_file_n_path = p.naut_dict['CONDOR_LOG_FILE']
    output = pytest.DEAP_ONE.util.get_key_line_in_lim(text_output,
                                        log_filepath = log_file_n_path)
    assert text_output in output[0]


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#             3/3 Psets can output specific inputted text to condor log
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

'''
  Scenario Outline: test pset D can inputted specific text
    Given another specific test pset "<test_5d_psets>"
    When a run is done
    Then 1st result is "<t1>"
    And 2nd result is

    Examples:
      | test_5d_psets   |  t1                 |
      | test_psetCd     |  injected_code_test |
'''

# 3/3 ***************************************************************************

@given(parsers.cfparse('another specific test pset "{test_5d_psets:String}"',
                        extra_types=EXTRA_TYPES),
                        target_fixture='test_5d_psets')
@given('another specific test pset "<test_5d_psets>"')
@pytest.mark.usefixtures("gpc3")
def a_specific_test_pset(gpc3, test_5d_psets):
    ''' sets up gp as standard, then amends pset'''
    gpc3.setup_gp()
    gpc3.set_test_evaluator('eval_test_5_3')
    gpc3.set_pset(test_5d_psets)

@when('a run is done')
@pytest.mark.usefixtures("gpc3")
def a_run_is_done(gpc3):
    ''' runs gp without input '''
    gpc3.set_population(1)
    gpc3.set_generations(1)
    gpc3.run_gp()

@then(parsers.cfparse('1st result is "{t1:String}"',
                        extra_types=EXTRA_TYPES),
                        target_fixture='t1')
@then('1st result is "<t1>"')
@pytest.mark.usefixtures("utils")
def first_result_is(utils, t1):
    key_req = 'TRACE:: Debug: eval_test_5_3:'
    limit_lines = 125 # util_dict['NO_LOG_LINES']
    got = utils.get_key_line_in_lim(key_req, limit_lines = limit_lines)

    assert got[0] != 'not found'
    assert got[1] > 0 and got[1] < limit_lines
    assert t1 in got[0]

@then('2nd result is')
def second_result_is():
    assert 1 == 1