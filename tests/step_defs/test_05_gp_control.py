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

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#             Lean tests each evolved individual
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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

# 'Successfully ran '.' in the 'backtesting' environment and stored the output in'

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
