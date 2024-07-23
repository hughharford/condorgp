import os
import os.path

import pytest
from pytest_bdd import scenarios, given, when, then, parsers
import logging
import shutil

from tests.conftest import *

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
pytest.logfile_n_path = ""
pytest.tidy_logs = 0

scenarios('../../features/up/10_util_keep_log_trim.feature')

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
def ensure_copy_of_long_file_available(params):
    ''' long log: tests/test_data/test_keep_logs_trim.json '''
    path = params.test_dict['CGP_TEST_DATA']
    source = path+"test_keep_logs_trim.json"
    destination = path+"test_log_file_to_trim.json"
    pytest.logfile_n_path = shutil.copyfile(source, destination)

@when(parsers.cfparse('the log file is above "{no_lines:Number}"',
                       extra_types=EXTRA_TYPES), target_fixture='no_lines')
@when('the log file is above "<no_lines>"')
def check_log_file_length(utils, no_lines):
    ''' check getting anything but not found '''
    current_lines = utils.count_lines_in_file(pytest.logfile_n_path)
    if current_lines > no_lines:
        pytest.tidy_logs = 1

@then(parsers.cfparse('the file is less than "{reduced_lines:Number}"',
                       extra_types=EXTRA_TYPES), target_fixture='reduced_lines')
@then('the file is less than "<reduced_lines>"')
def find_results(reduced_lines, utils):
    ''' check getting anything but nan '''
    log = pytest.logfile_n_path
    if pytest.tidy_logs == 1:
        utils.keep_x_lines_of_log(log, no_last_lines=reduced_lines-1)
    now_lines = utils.count_lines_in_file(pytest.logfile_n_path)
    assert reduced_lines >= now_lines

    # tidy up
def teardown_module():
    pass
    os.remove(pytest.logfile_n_path)
