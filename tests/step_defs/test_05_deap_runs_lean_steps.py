import os
import os.path

import pytest
from pytest_bdd import scenarios, given, when, then, parsers

# from condorgp.utils import get_last_x_log_lines
# from condorgp.utils import cp_config_to_lean_launcher
# from condorgp.utils import cp_ind_to_lean_algos
# from condorgp.utils import overwrite_main_with_input_ind
# from condorgp.utils import confirm_ind_name_in_log_lines
# from condorgp.utils import get_keyed_line_within_limits
# from condorgp.utils import get_last_chars

from condorgp.utils import Utils

from condorgp.params import lean_dict, test_dict, util_dict

from condorgp.lean_runner import RunLean

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

scenarios('../features/05_deap_runs_lean.feature')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#             Lean tests each evolved individual
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
  Scenario Outline: Lean is run and reports success and fitness
    Given a setup with Deap using Lean
    When Deap specs Lean to run "<input_ind>"
    Then the "<output_ind>" is found
    And the result: "<ROI_over_MDD_value>" is reported
    And the "<input_ind>" algorithm is tidied away

    Examples:
      | input_ind       |   output_ind       |   ROI_over_MDD_value    |
      | IndBasicAlgo1   |   IndBasicAlgo1    |   74.891                |
"""

# 'Successfully ran '.' in the 'backtesting' environment and stored the output in'

class UtilTest:
    def __init__(self) -> None:
        self.u = Utils()

@pytest.fixture
def utils():
    util = UtilTest()
    return util.u

@given('a setup with Deap using Lean')
def setup_ready():
    pass # assumes, rest of test to prove

@given(parsers.cfparse('Deap specs Lean to run "{input_ind:String}"',
                        extra_types=EXTRA_TYPES),
                        target_fixture='input_ind')
@given('Deap specs Lean to run "<input_ind>"', target_fixture='input_ind')
def copy_config_n_algo_across(input_ind):
    '''
    copies across config files and algorithms as needed
    '''
    copy_config_in(input_ind)
    copy_algo_in(input_ind)

def copy_config_in(utils, input_ind):
    # copy config.json across before container launch
    config_from_path = test_dict['CONDOR_CONFIG_PATH']
    if input_ind[-1] == '1':
        config_to_copy = test_dict['CONDOR_TEST_CONFIG_FILE_1']
    elif input_ind[-1] == '2':
        config_to_copy = test_dict['CONDOR_TEST_CONFIG_FILE_2']
    utils.cp_config_to_lean_launcher(config_from_path, config_to_copy)

def copy_algo_in(utils, input_ind):
    # copy algo.py across before container launch
    test_ind_path = test_dict['CONDOR_TEST_ALGOS_FOLDER']
    utils.cp_ind_to_lean_algos(test_ind_path, input_ind+'.py')
    utils.overwrite_main_with_input_ind(input_ind+'.py')


from condorgp.deap_condor import EvaluateWithLean

class MockedEvaluateWithLean(EvaluateWithLean):

    def __init__(ind_path_n_filename):
        super.__init__(ind_path_n_filename)

    def evaluate_with_lean():
        pass
