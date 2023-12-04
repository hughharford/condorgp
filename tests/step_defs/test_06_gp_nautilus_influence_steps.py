import os
import os.path

import pytest
from pytest_bdd import scenarios, given, when, then, parsers

from tests.fixtures import *
# from condorgp.params import lean_dict, test_dict, util_dict

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

pytest.MAXFITNESS = 0.0

scenarios('../features/06_gp_nautilus_influence.feature')

"""
Feature: GpControl's evolved code must affect Nautilus functionality
  As a gp algorithm,
  Evolved code created by GpControl needs to alter various characteristics,
  To ensure genuine fitness can be established.

  Scenario Outline: Evolved code shows Nautilus logged differences
    Given GpControl is run with "<pset_input>"
    When the evolved code is used
    Then Nautilus o/p is NEITHER "<expected_A>"
    And NOR is the Nautilus o/p "<expected_B>"

    Examples:
      | pset_input       |  expected_A         |   expected_B           |
      | naut_pset_01     |  -21.496631427091   |   -16.160361991815254  |
"""

@given(parsers.cfparse('GpControl is run with "{pset_input:String}"',
                        extra_types=EXTRA_TYPES),
                        target_fixture='pset_input')
@given('GpControl is run with  "<pset_input>"',
                        target_fixture='pset_input')
def gpcontrol_run_with(gp_control, pset_input):
    ''' sets one of two different psets '''
    gp_control.setup_gp(pset_spec=pset_input, pop_size=1, no_gens=1)

@when('the evolved code is used')
def injected_algo_includes(gp_control):
    gp_control.run_gp()

@then(parsers.cfparse('Nautilus o/p is NEITHER "{expected_A:Float}"',
                        extra_types=EXTRA_TYPES),
                        target_fixture='expected_A')
@then('Nautilus o/p is NEITHER "<expected_A>"',
                        target_fixture='expected_A')
def output_isnt_mdd(gp_control, expected_A):
    pytest.MAXFITNESS = gp_control.gp.logbook.select("max")[-1]
    print(pytest.MAXFITNESS)
    assert pytest.MAXFITNESS != expected_A

@then(parsers.cfparse('NOR is the Nautilus o/p "{expected_B:Float}"',
                        extra_types=EXTRA_TYPES),
                        target_fixture='expected_B')
@then('NOR is the Nautilus o/p "<expected_B>"',
                        target_fixture='expected_B')
def output_isnt_mdd(gp_control, expected_B):
    # max_fitness_found = gp_control.gp.logbook.select("max")[-1]
    # print(max_fitness_found)
    assert pytest.MAXFITNESS != expected_B
