import os
import os.path

import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from condorgp.params import Params

from gp_fixtures import gp_control

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

scenarios('../../features/up/005_gp_control.feature')

@given('a specific pset is needed')
def setup_ready(gp_control):
    cp_freq = 0
    gp_control.set_gp_n_cp(freq=cp_freq, cp_file="empty")

@when(parsers.cfparse('GpControl gets a requirement for "{pset_input:String}"',
      extra_types=EXTRA_TYPES), target_fixture='pset_input')
@when('GpControl gets a requirement for "<pset_input>"',
      target_fixture='pset_input')
def check_GpControl(gp_control, pset_input):
    ''' sets 2 different psets '''

    gp_control.base_pset = gp_control.set_and_get_pset('test_base_pset')
    gp_control.test_pset = gp_control.set_and_get_pset(pset_input)

@when('GpControl is checked')
def check_gp_control(gp_control):
    assert type(gp_control.base_pset) is not None
    assert type(gp_control.test_pset) is not None

@then('the pset returned is not the same as the base_pset')
def pset_returned_is(gp_control):
    assert gp_control.base_pset != gp_control.test_pset

@then(parsers.cfparse('the pset returns contains "{primitive_name:String}"',
                      extra_types=EXTRA_TYPES), target_fixture='primitive_name')
@then('the pset returns contains "<primitive_name>"')
def pset_contains(gp_control, primitive_name):
    assert gp_control.test_pset
    prim_names = list(gp_control.test_pset.context.keys())
    assert primitive_name in prim_names
