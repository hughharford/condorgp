import os
import os.path

import pytest
from pytest_bdd import scenarios, given, when, then, parsers

from tests.fixtures import gpc, gpc2, utils # these go dark, but without
from condorgp.params import lean_dict, test_dict, util_dict

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
      | psetA           |  mul          |
      | psetB           |  add          |
"""
# ***************************************************************************

@given('a specific pset is needed')
def setup_ready():
    pass # assumes, rest of test to prove

@when(parsers.cfparse('GpControl gets a requirement for "{pset_input:String}"',
                        extra_types=EXTRA_TYPES),
                        target_fixture='input_ind')
@when('GpControl gets a requirement for "<pset_input>"',
        target_fixture='pset_input')
@pytest.mark.usefixtures("gpc")
def check_GpControl(gpc, pset_input):
    ''' sets 2 different psets '''
    gpc.base_pset = gpc.set_pset('test_base_pset')
    gpc.test_pset = gpc.set_pset(pset_input)

@when('GpControl is checked')
def check_gp_control(gpc):
    assert type(gpc.base_pset) is not None
    assert type(gpc.test_pset) is not None

@then('the pset returned is not the same as the base_pset')
def pset_returned_is(gpc):
    assert gpc.base_pset != gpc.test_pset

@then(parsers.cfparse('the pset returns contains "{primitive_name:String}"',
                        extra_types=EXTRA_TYPES),
                        target_fixture='primitive_name')
@then('the pset returns contains "<primitive_name>"')
def pset_contains(gpc, primitive_name):
    assert gpc.test_pset
    prim_names = list(gpc.test_pset.context.keys())
    assert primitive_name in prim_names


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#             2/3 Running a pset can output log text
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

'''
  Scenario Outline: test psets can output specific text to condor log
    Given a specific test pset "<test_psetC_untyped>"
    When provided the "<arg_input>"
    Then the result is "<text_output>"

    Examples:
      | arg_input     | pset_input              |  text_output        |
      | hello_world   | test_psetC_untyped      |  hello_world        |
'''

# ***************************************************************************

@given(parsers.cfparse('a specific test pset "{test_C_psets:String}"',
                        extra_types=EXTRA_TYPES),
                        target_fixture='test_C_psets')
@given('a specific test pset "<test_C_psets>"')
@pytest.mark.usefixtures("gpc")
def setup_ready(gpc, test_C_psets):
    ''' sets up gp as standard, then amends pset'''
    gpc.setup_gp()
    gpc.set_test_evaluator()
    gpc.set_pset(test_C_psets)

@when(parsers.cfparse('provided the "{arg_input:String}"',
                        extra_types=EXTRA_TYPES),
                        target_fixture='arg_input')
@when('provided the "<arg_input>"',
        target_fixture='arg_input')
def provided_the(gpc, arg_input):
    ''' runs gp with arg_input as given '''
    gpc.set_population(50)
    gpc.set_generations(5)
    gpc.run_gp(arg_input)

@then(parsers.cfparse('the result is "{text_output:String}"',
                        extra_types=EXTRA_TYPES),
                        target_fixture='text_output')
@then('the result is "<text_output>"')
def condor_log_contains(gpc, text_output):
    ''' checks condor log for text expected '''
    log_file_n_path = util_dict['CONDOR_LOG']
    output = gpc.util.get_keyed_line_in_limits(text_output,
                                        log_file_n_path = log_file_n_path)
    print(output)
    assert text_output in output[0]


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#             3/3 Psets can output specific inputted text to condor log
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

'''
  Scenario Outline: test pset D can output specific inputted text to Lean log
    Given a specific test pset "<test_D_psets>"
    When a run is done
    Then 1st result is "<t1>"
    And 2nd result is

    Examples:
      | test_D_psets    |  t1                 |
      | test_psetC      |  hello_world        |
      | test_psetCi     |  hi_hi_hi_hi        |
'''

# ***************************************************************************

@given(parsers.cfparse('a specific test pset "{test_D_psets:String}"',
                        extra_types=EXTRA_TYPES),
                        target_fixture='test_D_psets')
@given('a specific test pset "<test_C_psets>"')
@pytest.mark.usefixtures("gpc2")
def setup_ready(gpc2, test_C_psets):
    ''' sets up gp as standard, then amends pset'''
    gpc2.setup_gp()
    gpc2.set_test_evaluator()
    gpc2.set_pset(test_C_psets)

@when('a run is done')
def provided_the(gpc2):
    ''' runs gp without input '''
    gpc2.set_population(5)
    gpc2.set_generations(5)
    gpc2.run_gp()

@then(parsers.cfparse('1st result is "{t1:String}"',
                        extra_types=EXTRA_TYPES),
                        target_fixture='t1')
@then('the result is "<t1>"')
def first_result(gpc2, t1):
    assert gpc2.test_pset
    pass
    assert 1 == 1
