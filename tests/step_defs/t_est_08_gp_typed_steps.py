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

scenarios('../features/08_gp_typed.feature')

"""
  Scenario Outline: Evolved code can be run
    Given GpControl with "<pset_input_08>"
    When 08 Lean run with enough pop & gen
    Then 08 fitness is above zero
    And 08 shows fitness increasing

    Examples:
      | pset_input_08   |
      | test_pset8a     |
      | test_pset8b     |
"""
@given(parsers.cfparse('GpControl with "{pset_input_08:String}"',
                        extra_types=EXTRA_TYPES), target_fixture='pset_input_08')
@given('GpControl with "<pset_input_08>"', target_fixture='<pset_input_08>')
@pytest.mark.usefixtures("gpc")
def gpcontrol_with_typed_psets08(gpc, pset_input_08):
    pop = 5
    gen = 3
    gpc.setup_gp(pset_input_08, pop, gen)
    gpc.set_test_evaluator('eval_test_8')

@when('08 Lean run with enough pop & gen')
def lean_08_with_enough_p_n_g(gpc):
    gpc.run_gp()

@then('08 fitness is above zero')
def fitness_08_is(gpc):
    max_fitness_found = gpc.gp.logbook.select("max")[-1]
    assert max_fitness_found > 0

@then('08 shows fitness increasing')
def shows_08_fitness_increasing(gpc):
    max_fitness_found = gpc.gp.logbook.select("max")[-1]
    min_fitness_found = gpc.gp.logbook.select("min")[0]
    print(f'min = {min_fitness_found}, max = {max_fitness_found}')
    assert max_fitness_found > min_fitness_found
