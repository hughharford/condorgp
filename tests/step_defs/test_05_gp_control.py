import os
import os.path

import pytest
from pytest_bdd import scenarios, given, when, then, parsers

from tests.fixtures import gpc, utils # these go dark, but without
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
#             GpControl can set different psets as needed
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
    '''  '''
    # if hasattr(gpc, 'base_pset'):
    #     assert 1 == 4
    # else:
    #     # assert 3 == 5
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
#             GpControl can set different psets as needed
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

'''
  Scenario Outline: test psets can output specific text
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
    gpc.set_population(100)
    gpc.set_generations(5)
    gpc.run_gp(arg_input)

@then(parsers.cfparse('the result is "{text_output:String}"',
                        extra_types=EXTRA_TYPES),
                        target_fixture='text_output')
@then('the result is "<text_output>"')
def pset_contains(gpc, text_output):
    pass
    assert 1 == 1
