import os
import sys
from datetime import datetime

from pytest_bdd import scenarios, given, when, then, parsers

from condorgp.utils import run_lean_bash_script
from condorgp.params import lean_dict

EXTRA_TYPES = {
    'Number': int,
    'String': str,
}

CONVERTERS = {
    'initial': int,
    'some': int,
    'total': int,
}

scenarios('../features/02_lean_results.feature')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#             Lean runs and outputs results
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
Scenario: Basic Lean run
    Given lean:latest docker image
    And run_docker.sh file
    When run_docker.sh is run
    Then leanQC/results files are updated
"""

@given('lean:latest docker image')
def docker_image_exists():
    pass # assumes local lean:latest image extant

@given('run_docker.sh file')
def run_docker_shell_file_exists():
    sh_file_path = 'leanQC/run_docker.sh'
    assert os.path.exists(sh_file_path)

@when('run_docker.sh is run')
def call_run_docker():
    run_lean_bash_script()
    pass

@then('leanQC/results files are updated')
def results_files_are_updated():
    results_path = lean_dict['LEAN_RESULTS_FOLDER']
    results_files = [results_path + x for x in os.listdir(results_path)]
    assert len(results_files) > 1
    assert check_recent_mod(results_files)

def check_recent_mod(input_file_paths):
    dt = datetime.now()
    now = datetime.timestamp(dt)
    diff = 1000*lean_dict['REASONABLE_FITNESS_SECS']
    for file_path in input_file_paths:
        if (now - diff) > os.path.getmtime(file_path): return False
    return True
