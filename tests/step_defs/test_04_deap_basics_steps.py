import pytest
import numpy
from pytest_bdd import scenarios, given, when, then

from condorgp.params import lean_dict, test_dict, util_dict
from condorgp.deap_condor import CondorDeap

from deap import gp
# /home/hsth/code/hughharford/condorgp/condorgp/deap_with_lean.py

scenarios('../features/04_deap_basics.feature')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#             Deap basic operations
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
  Scenario Outline: Deap instanciation includes functions
    Given Deap is setup
    When an instance of Deap is instantiated
    And the functions are listed
    Then the fundamental functions are found
"""
class DeapTester:
    def __init__(self) -> None:
        self.ourdeap = CondorDeap()

    # def get_deap(self):
    #     return self.ourdeap

@pytest.fixture
def get_one():
    a = DeapTester()
    return a.ourdeap

@given('Deap is setup')
def deap_ready(get_one):
    assert get_one is not None

@when('an instance of Deap is instantiated')
def instantiated_deap(get_one):
    print(get_one)
            # primitive set:
    get_one.pset = gp.PrimitiveSet("MAIN", 1)
    get_one.pset.addPrimitive(numpy.add, 2, name="vadd")
    get_one.pset.addPrimitive(numpy.subtract, 2, name="vsub")
    get_one.pset.addPrimitive(numpy.multiply, 2, name="vmul")
    get_one.pset.addPrimitive(numpy.negative, 1, name="vneg")
    get_one.pset.addPrimitive(numpy.cos, 1, name="vcos")
    get_one.pset.addPrimitive(numpy.sin, 1, name="vsin")
    get_one.pset.addTerminal(1)
    get_one.pset.addTerminal(5)


@when('the functions are listed')
def get_deap_functions(get_one):
    get_one.log.info(f'primitives_count = {get_one.pset.prims_count}')
    get_one.log.info(f'terminals_count = {get_one.pset.terms_count}')
    print("NOTE: count of terminals includes base terminal class => -1")

    assert get_one.pset.prims_count == 6
    assert get_one.pset.terms_count - 1 == 2


@then('the fundamental functions are found')
def check_deap_functions_match():
    assert 1 == 1
    pass # nothing to do here
