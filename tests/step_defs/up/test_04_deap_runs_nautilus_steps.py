import os
import os.path

import pytest
from pytest_bdd import scenarios, given, when, then, parsers
import logging

from tests.fixtures import *

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

pytest.foundfitness = 99

scenarios('../../features/up/04_deap_runs_nautilus.feature')

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
    When a short Deap run is conducted
    Then the result is not "<not_found_code>"
    And the result is neither "<nan_code>"

    Examples:
      | input_ind  |   not_found_code    |  nan_code   |
      | default    |   111000            |  22000      |
"""

@given('a setup with Deap using Nautilus')
def setup_ready():
    ''' assumed setup ready '''
    pass # assumed, nothing operates otherwise

@when('a short Deap run is conducted')
def short_deap_run(gpc):
    ''' shortest deap run possible '''
    assert gpc is not None
    pset_used = 'naut_pset_01' # 'test_pset5c'
    newpop = 1
    gens = 1

    cp_freq = 0
    gpc.set_gp_n_cp(freq=cp_freq, cp_file="empty")

    gpc.setup_gp(pset_used, newpop, gens)
    gpc.run_gp()

@then(parsers.cfparse('the result is not "{not_found_code:Float}"',
                       extra_types=EXTRA_TYPES), target_fixture='not_found_code')
@then('the result is not "<not_found_code>"')
def find_results(not_found_code, gpc):
    ''' check getting anything but not found '''
    max_fitness_found = gpc.gp.logbook.select("max")[-1]
    pytest.foundfitness = max_fitness_found
    assert not_found_code != max_fitness_found

@then(parsers.cfparse('the result is neither "{nan_code:Float}"',
                       extra_types=EXTRA_TYPES), target_fixture='nan_code')
@then('the result is neither "<nan_code>"')
def find_results(nan_code):
    ''' check getting anything but nan '''
    assert nan_code != pytest.foundfitness
