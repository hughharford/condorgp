import os
import os.path

import pytest
from pytest_bdd import scenarios, given, when, then, parsers

from tests.fixtures import deap_one, utils
# from condorgp.params import test_dict, util_dict

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

scenarios('../../features/04_deap_runs_nautilus.feature')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    Deap runs Nautilus tests for each evolved individual
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
Feature: Simple usage of Nautilus by Deap, connecting the two
  As an evoluationary algorithm,
  Deap needs to use Nautilus to evaluate,
  To test each invidual.

  Scenario Outline: Nautilus is run and reports success and fitness
    Given a setup with Deap using Nautilus
    When Deap specs Nautilus to run "<input_ind>"
    And a short Deap run is conducted
    Then the result: "<expected_value>" is found

    Examples:
      | input_ind       |   expected_value          |
      | default         |   -21.496631427091        |
"""

# 'Successfully ran '.' in the 'backtesting' environment and stored the output in'

@given('a setup with Deap using Nautilus')
def setup_ready():
    pass # assumed

@when(parsers.cfparse('Deap specs Nautilus to run "{input_ind:String}"',
                        extra_types=EXTRA_TYPES),
                        target_fixture='input_ind')
@when('Deap specs Nautilus to run "<input_ind>"', target_fixture='input_ind')
def deap_sets_algo_to_nautilus(utils, input_ind):
    ''' copies across config files and algorithms as needed '''
    pass # nothing to do, no longer pass across algorithms

@when('a short Deap run is conducted')
def short_deap_run(deap_one):
    assert deap_one is not None
    newpop = 1
    gens = 1
    deap_one.setup_gp('', newpop, gens)
    deap_one.run_gp()

@then(parsers.cfparse('the result: "{expected_value:Float}" is found',
                       extra_types=EXTRA_TYPES), target_fixture='expected_value')
@then('the result: "<expected_value>" is found')
def find_results(expected_value, deap_one):
    max_fitness_found = deap_one.gp.logbook.select("max")[-1]
    assert expected_value >= max_fitness_found
