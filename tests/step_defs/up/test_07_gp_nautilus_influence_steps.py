import os
import os.path

import pytest
from pytest_bdd import scenarios, given, when, then, parsers

from gp_fixtures import gp_control

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

scenarios('../../features/up/07_gp_nautilus_influence.feature')

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
    ''' sets psets for nautilus 1st config setup '''
    eval_used = 'eval_nautilus'
    p = 1
    g = 1
    cp_freq = 0
    gp_control.set_gp_n_cp(freq=cp_freq, cp_file="empty")
    gp_control.setup_gp(pset_spec=pset_input, pop_size=p, no_gens=g)
    gp_control.set_test_evaluator(eval_used)

@when('the evolved code is used')
def injected_algo_includes(gp_control):
    ''' starts gp run with set parameters '''
    gp_control.initiate_gp_run()

@then(parsers.cfparse('Nautilus o/p is NEITHER "{expected_A:Float}"',
                        extra_types=EXTRA_TYPES),
                        target_fixture='expected_A')
@then('Nautilus o/p is NEITHER "<expected_A>"',
                        target_fixture='expected_A')
def output_isnt_mdd(gp_control, expected_A):
    ''' confirms a different fitness to A '''
    pytest.MAXFITNESS = gp_control.gp.logbook.select("max")[-1]
    print(pytest.MAXFITNESS)
    assert pytest.MAXFITNESS != expected_A

@then(parsers.cfparse('NOR is the Nautilus o/p "{expected_B:Float}"',
                        extra_types=EXTRA_TYPES),
                        target_fixture='expected_B')
@then('NOR is the Nautilus o/p "<expected_B>"',
                        target_fixture='expected_B')
def output_isnt_mdd(expected_B):
    ''' confirms a different fitness to B '''
    assert pytest.MAXFITNESS != expected_B
