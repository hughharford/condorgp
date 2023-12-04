import os
import os.path

import pytest
from pytest_bdd import scenarios, given, when, then, parsers

from tests.fixtures import gpc # utils # these go dark, but without
from condorgp.params import lean_dict, test_dict, util_dict

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

scenarios('../tests/features/07_gp_fitmax.feature')

"""
  Scenario Outline: Evolved code shows fitness improvement
    Given GpControl is run with test_pset7aTyped
    When the injected algo runs with 7aT
    Then fitness improves over the generations run
"""

@given('GpControl is run with test_pset7aTyped')
@pytest.mark.usefixtures("gpc")
def gpcontrol_run_with_typed7a(gpc):
    pop = 5
    gen = 3
    gpc.setup_gp('test_pset7aTyped', pop, gen)
    gpc.set_test_evaluator('eval_test_6')

@when('the injected algo runs with 7aT')
def injected_algo_runs_7aT(gpc):
    gpc.run_gp()

@then('fitness improves over the generations run')
def fitness_shown_to_increase(gpc):
    max_fitness_found = gpc.gp.logbook.select("max")[-1]
    min_fitness_found = gpc.gp.logbook.select("min")[0]
    print(f'min = {min_fitness_found}, max = {max_fitness_found}')
    assert max_fitness_found > min_fitness_found
    # THIS tidy up now built into GpControl
#    utils.del_pys_from_local_packages()
