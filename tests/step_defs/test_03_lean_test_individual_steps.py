import os

from pytest_bdd import scenarios, given, when, then, parsers

from condorgp.utils import run_lean_via_CLI
from condorgp.utils import copy_config_json_to_lean_launcher_dir
from condorgp.utils import copy_ind_to_lean_algos_dir
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

@given(parsers.cfparse('an evolved "{input_ind:String}" is specified',
                       extra_types=EXTRA_TYPES), target_fixture='input_ind')
@given('an evolved "<input_ind>" is specified', target_fixture='input_ind')
def copy_config_n_algo_across(input_ind):
    # copy config.json across before container launch
    config_to_copy = test_dict['CONDOR_TEST_CONFIG_FILE']
    config_path = test_dict['CONDOR_CONFIG_PATH']
    copy_config_json_to_lean_launcher_dir(config_path, config_to_copy)

    # copy algo.py across before container launch
    test_ind_path = test_dict['CONDOR_TEST_ALGOS_FOLDER']
    copy_ind_to_lean_algos_dir(test_ind_path, input_ind + '.py')


@when('Lean runs')
def set_lean_runner():
    '''uses the utils method to set an os system command via Lean CLI'''
    run_lean_via_CLI()

@then(parsers.cfparse('the "{output_ind:String}" is found',
                       extra_types=EXTRA_TYPES), target_fixture='output_ind')
@then('the "<output_ind>" is found', target_fixture='output_ind')
def results_files_are_updated(output_ind):
    results_path = lean_dict['LEAN_RESULTS_FOLDER']
    output_ind = results_path + output_ind
    # 'leanQC/results/BasicTemplateFrameworkAlgorithm'
    results_files = [results_path + x for x in os.listdir(results_path)]
    found_algo_name = False
    for folder_or_file in results_files:
        if folder_or_file == output_ind:
            found_algo_name = True
    assert found_algo_name

####### TEST AGAINST THE FOLLOWING INSTEAD:


# near start:
# Compiling '/LeanCLI/IndBasicAlgo1.py'...
# 20220718 21:00:45.997 TRACE:: JobQueue.NextJob(): Selected
# /LeanCLI/IndBasicAlgo1.py

# 2022-07-18T20:50:21.3422736Z TRACE:: Engine.Main(): Started 8:50 PM

# then, further down:
# [GCC 7.3.0]: Importing python module IndBasicAlgo1
# 2022-07-18T20:50:24.8145994Z TRACE:: AlgorithmPythonWrapper(): IndBasicAlgo1 successfully imported.
