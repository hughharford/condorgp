import os
import sys
from datetime import datetime

from pytest_bdd import scenarios, given, when, then, parsers

from condorgp.utils import run_lean_bash_script
from condorgp.utils import copy_config_json_to_lean_launcher_dir
from condorgp.params import lean_dict, test_dict

EXTRA_TYPES = {
    'Number': int,
    'String': str,
}

CONVERTERS = {
    'initial': int,
    'some': int,
    'total': int,
}

scenarios('../features/03_lean_test_individual.feature')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#             Lean tests each evolved individual
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
Scenario Outline: Lean tests each individual
    Given a Lean container ready to run
    And an evolved "<individual>" is specified
    When Lean runs
    Then the "<individual>" is used
"""

# LEAN_ALGOS_FOLDER
# copy_ind_to_lean_algos_dir

@given('a Lean container ready to run')
def lean_container_tested_already():
    pass # assumes local lean:latest image extant

@given(parsers.cfparse('an evolved "{individual:String}" is specified', extra_types=EXTRA_TYPES), target_fixture='individual')
@given('an evolved "<individual>" is specified')
def copy_config_to_raw_launcher_dir(individual):
    test_ind_path = test_dict['CONDOR_TEST_ALGOS_FOLDER']
    copy_config_json_to_lean_launcher_dir(test_ind_path + individual + '.py')

@when('Lean runs')
def run_lean():
    run_lean_bash_script()
    pass

@given(parsers.cfparse('the "{individual:String}" is used', extra_types=EXTRA_TYPES), target_fixture='individual')
@then('the "<individual>" is used')
def results_files_are_updated(individual):
    results_path = lean_dict['LEAN_RESULTS_FOLDER']
    results_files = [results_path + '/' + x for x in os.listdir(results_path)]
    assert results_files[0] == individual
