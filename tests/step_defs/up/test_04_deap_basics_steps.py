import numpy
import pytest
from pytest_bdd import scenarios, given, when, then
from deap import gp

from tests.fixtures import *

scenarios('../../features/04_deap_basics.feature')

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
@pytest.mark.usefixtures("deap_one")
@given('Deap is setup')
def deap_ready(deap_one):
    assert deap_one is not None

@when('an instance of Deap is instantiated')
def instantiated_deap(deap_one):
    print(deap_one)
            # primitive set:
    deap_one.pset = gp.PrimitiveSet("MAIN", 1)
    deap_one.pset.addPrimitive(numpy.add, 2, name="vadd")
    deap_one.pset.addPrimitive(numpy.subtract, 2, name="vsub")
    deap_one.pset.addPrimitive(numpy.multiply, 2, name="vmul")
    deap_one.pset.addPrimitive(numpy.negative, 1, name="vneg")
    deap_one.pset.addPrimitive(numpy.cos, 1, name="vcos")
    deap_one.pset.addPrimitive(numpy.sin, 1, name="vsin")
    deap_one.pset.addTerminal(1)
    deap_one.pset.addTerminal(5)


@when('the functions are listed')
def get_deap_functions(deap_one):
    deap_one.log.info(f'primitives_count = {deap_one.pset.prims_count}')
    deap_one.log.info(f'terminals_count = {deap_one.pset.terms_count}')
    print("NOTE: count of terminals includes base terminal class => -1")

    assert deap_one.pset.prims_count == 6
    assert deap_one.pset.terms_count - 1 == 2


@then('the fundamental functions are found')
def check_deap_functions_match():
    assert 1 == 1
    pass # nothing to do here
