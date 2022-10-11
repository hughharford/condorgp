import os
import os.path

import pytest
from pytest_bdd import scenarios, given, when, then, parsers

from tests.fixtures import gpc, utils # these go dark, but without
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

scenarios('../features/06_gp_lean_influence.feature')

"""
  Scenario Outline: Evolved code shows Lean logged differences
    Given GpControl is run with "<pset_input>"
    When the injected algo inc "<object_input>"
    Then Lean o/p is NOT "<RoMDD>"

    Examples:
      | pset_input       | alpha_terminal    |  RoMDD                   |
      | test_pset6a      | alpha_a           |  110.382                 |
      | test_pset6b      | alpha_b           |  110.382                 |
"""

@given(parsers.cfparse('GpControl is run with "{pset_input:String}"',
                        extra_types=EXTRA_TYPES), target_fixture='pset_input')
@given('GpControl is run with  "<pset_input>"', target_fixture='pset_input')
@pytest.mark.usefixtures("gpc")
def gpcontrol_run_with(gpc, pset_input):
    ''' sets one of two different psets '''
    gpc.setup_gp()
    gpc.set_test_evaluator('eval_test_6')
    gpc.set_pset(pset_input)

@when('the injected algo is varied')
def injected_algo_includes(gpc):
    gpc.set_population(10)
    gpc.set_generations(1)
    gpc.run_gp()

@then(parsers.cfparse('Lean o/p is NOT "{RoMDD:Float}"',
                        extra_types=EXTRA_TYPES),
                        target_fixture='RoMDD')
@then('Lean o/p is NOT "<RoMDD>"', target_fixture='RoMDD')
@pytest.mark.usefixtures("utils")
def output_isnt_mdd(utils, gpc, RoMDD):
    max_fitness_found = gpc.gp.logbook.select("max")[-1]
    print(max_fitness_found)
    assert max_fitness_found
    # THEN TIDY UP TOO
    utils.del_pys_from_local_packages()
