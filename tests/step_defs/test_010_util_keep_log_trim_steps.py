import os
import os.path

import pytest
from pytest_bdd import scenarios, given, when, then, parsers
import logging

from tests.fixtures import utils

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

scenarios('../features/010_util_keep_log_trim.feature')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    Deap runs Nautilus tests for each evolved individual
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
Feature: Usage of Nautilus by Deap, creates long logs
  As an evoluationary algorithm,
  Many runs will be made, we need to avoid accumulating massive logs,
  To avoid large files, and their costs.

  Scenario Outline: Deap runs Nautilus and logs are trimmed
    Given a long log file
    When the log file is above "<no_lines>"
    Then the file is less than "<reduced_lines>"

    Examples:
      |   no_lines   |  reduced_lines  |
      |   20000      |  10001          |

"""

@given('a long log file')
def setup_ready():
    ''' long log: tests/test_data/test_keep_logs_trim.json '''
    pass

@when(parsers.cfparse('the log file is above "{no_lines:Number}"',
                       extra_types=EXTRA_TYPES), target_fixture='no_lines')
@when('the log file is above "<no_lines>"')
def check_log_file_length(utils, no_lines):
    ''' check getting anything but not found '''
    pass

@then(parsers.cfparse('the file is less than "{reduced_lines:Number}"',
                       extra_types=EXTRA_TYPES), target_fixture='reduced_lines')
@then('the file is less than "<reduced_lines>"')
def find_results(reduced_lines):
    ''' check getting anything but nan '''
    no_log_lines = 10_000_000
    assert reduced_lines > no_log_lines
