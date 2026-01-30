import os
import os.path

import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from condorgp.gp.gp_functions import GpFunctions
# from condorgp.params import Params

from gp_fixtures import params, utils, gpf


pytest.r_name_1 = ""
pytest.r_name_2 = ""
pytest.log1 = ""
pytest.log2 = ""

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

scenarios('../../features/up/006_gp_find_fitness.feature')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#             find_fitness correctly return fitness
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# SCENARIO 1
# ===============================================================
@given('the test_find_fitness_1.json')
def check_json_in_test_data_1(utils, params):
    ''' confirms test json log in place '''
    json_path = params.test_dict["CGP_TEST_DATA"]+"test_find_fitness_1.json"
    false_json_path = params.test_dict["CGP_TEST_DATA"]+"test_find_fitness_3.json"
    assert utils.confirm_file_extant(json_path)
    assert not utils.confirm_file_extant(false_json_path)
    pytest.log1 = json_path

@when(parsers.cfparse('find_fitness gets fitness for "{naut_runner:String}"',
      extra_types=EXTRA_TYPES), target_fixture='naut_runner')
@when('find_fitness gets fitness for "<naut_runner>"',
      target_fixture='naut_runner')
def nautilus_runner_1(naut_runner):
    ''' purely for reference '''
    pass # it's the runner_name that is searched

@when(parsers.cfparse('the runner name is "{runner_name:String}"',
extra_types=EXTRA_TYPES), target_fixture='runner_name')
@when('the runner name is "<runner_name>"',
      target_fixture='runner_name')
def runner_name_1(runner_name):
    ''' criteria for which runner's output to search for '''
    # it's the runner_name that is searched
    pytest.r_name_1 = runner_name

@then(parsers.cfparse('the fitness found is "{sharpe_ratio:String}"',
                      extra_types=EXTRA_TYPES), target_fixture='sharpe_ratio')
@then('the fitness found is "<sharpe_ratio>"')
def fitness_found_is_1(gpf, sharpe_ratio):
    ''' check sharpe's ratio reported is as expected '''
    assert float(sharpe_ratio) == gpf.find_fitness(backtest_id=pytest.r_name_1,
                                                   log_file_n_path=pytest.log1)


# SCENARIO 2
# ===============================================================

@given('the test_find_fitness_2.json')
def check_json_in_test_data_2(utils, params):
    ''' confirms test json log in place '''
    json_path = params.test_dict["CGP_TEST_DATA"]+"test_find_fitness_2.json"
    assert utils.confirm_file_extant(json_path)
    pytest.log2 = json_path

@when(parsers.cfparse('find_fitness gets the latest fitness for "{naut_runner:String}"',
      extra_types=EXTRA_TYPES), target_fixture='naut_runner')
@when('find_fitness gets the latest fitness for "<naut_runner>"',
      target_fixture='naut_runner')
def nautilus_runner_2(naut_runner):
    ''' purely for reference '''
    pass # it's the runner_name that is searched


@when(parsers.cfparse('checks the runner name is "{runner_name:String}"',
      extra_types=EXTRA_TYPES), target_fixture='runner_nam=e')
@when('checks the runner name is "<runner_name>"',
      target_fixture='runner_name')
def runner_name_2(runner_name):
    ''' criteria for which runner's output to search for '''
    # it's the runner_name that is searched
    pytest.r_name_2 = runner_name

@then(parsers.cfparse('the latest fitness found is "{sharpe_ratio:String}"',
                      extra_types=EXTRA_TYPES), target_fixture='sharpe_ratio')
@then('the latest fitness found is "<sharpe_ratio>"')
def fitness_found_is_2(gpf, sharpe_ratio):
    ''' check sharpe's ratio reported is as expected '''
    assert float(sharpe_ratio) == gpf.find_fitness(backtest_id=pytest.r_name_2,
                                                   log_file_n_path=pytest.log2)
