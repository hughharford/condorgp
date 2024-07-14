import numpy
import pytest
from pytest_bdd import scenarios, given, when, then
from deap import gp
import logging
from tests.gpc_fixtures import *
from condorgp.factories.factory import Factory


pytest.DEAP_ONE = ""

scenarios('../../features/up/03_deap_basics.feature')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#             Deap basic operations
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
  Scenario Outline: Deap instanciation includes functions
    Given Deap is setup
    When an instance of Deap is instantiated
    And the functions are added
    Then the fundamental functions are found
"""
@given('Deap is setup')
def deap_ready(gp_control):
    Factory().start_logger()
    assert gp_control is not None

@when('an instance of Deap is instantiated')
def instantiated_deap(gp_control):
    '''
        Instantiated Deap.
    '''
    # print(deap_one)
    pytest.DEAP_ONE = gp_control
    logging.info(f'pytest.DEAP_ONE: {gp_control}')

@when('the functions are added')
def get_deap_functions():
    pytest.DEAP_ONE.pset = gp.PrimitiveSet("MAIN", 1)
    pytest.DEAP_ONE.pset.addPrimitive(numpy.add, 2, name="vadd")
    pytest.DEAP_ONE.pset.addPrimitive(numpy.subtract, 2, name="vsub")
    pytest.DEAP_ONE.pset.addPrimitive(numpy.multiply, 2, name="vmul")
    pytest.DEAP_ONE.pset.addPrimitive(numpy.negative, 1, name="vneg")
    pytest.DEAP_ONE.pset.addPrimitive(numpy.cos, 1, name="vcos")
    pytest.DEAP_ONE.pset.addPrimitive(numpy.sin, 1, name="vsin")
    pytest.DEAP_ONE.pset.addTerminal(1)
    pytest.DEAP_ONE.pset.addTerminal(5)


@then('the fundamental functions are found')
def check_deap_functions_match():
    logging.info(
        f'primitives_count = {pytest.DEAP_ONE.pset.prims_count}')
    logging.info(
        f'terminals_count = {pytest.DEAP_ONE.pset.terms_count}')
    print("NOTE: count of terminals includes base terminal class => -1")

    assert pytest.DEAP_ONE.pset.prims_count == 6
    assert pytest.DEAP_ONE.pset.terms_count - 1 == 2
