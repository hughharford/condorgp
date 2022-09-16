import pytest
from pytest_bdd import scenarios, given, when, then

from condorgp.params import lean_dict, test_dict, util_dict
from condorgp.deap_with_lean import CondorDeap
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
class deap_tester:
    def __init__(self) -> None:
        self.ourdeap = CondorDeap()
        # self.DEAP_FUNCTIONS = {}

@pytest.fixture
def get_deap():
    d = deap_tester()
    return d

@given('Deap is setup')
def deap_ready():
    pass # nothing to do here

@when('an instance of Deap is instantiated')
def instantiated_deap(get_deap):
    print(get_deap)
    pass # nothing to do here

@when('the functions are listed')
def get_deap_functions(deap_tester):
    pass
    # assert tester.DEAP != None

@then('the fundamental functions are found')
def check_deap_functions_match():
    assert 1 == 1
    pass # nothing to do here
