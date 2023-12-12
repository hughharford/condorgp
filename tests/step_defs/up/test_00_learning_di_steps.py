from pytest_bdd import scenarios, given, when, then, parsers

from tests.fixtures import *

scenarios('../../features/up/00_learning_di.feature')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#             REAL AND MOCK DEPENDENCIES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
Scenario: With the original dependency
    Given a fixture providing the class
    When the dependency is instantiated
    Then dep_multiply returns 1000 * our value
    Then dep_add returns our value + 1000

Scenario: With our mocked dependency
    Given a fixture providing the mocked class
    When the mocked dependency is instantiated
    Then dep_multiply mock returns 5000 * our value
    Then dep_add mock returns our value + 5000
"""

INPUT = 7

@pytest.mark.usefixtures("dep_di")
@given('a fixture providing the class')
def with_dependency(dep_di):
    assert dep_di is not None

@pytest.mark.usefixtures("dep_di_mock")
@given('a fixture providing the mocked class')
def with_mocked_dependency(dep_di_mock):
    assert dep_di_mock is not None

@when('the dependency is instantiated')
def use_dependency(dep_di):
    assert (dep_di.dep_add(INPUT) * dep_di.dep_multiply(INPUT)) != 0

@when('the mocked dependency is instantiated')
def use_mocked_dependency(dep_di_mock):
    assert (dep_di_mock.dep_add(INPUT) * dep_di_mock.dep_multiply(INPUT)) != 0

@then('dep_multiply returns 1000 * our value')
def check_multiplication(dep_di):
    assert dep_di.dep_multiply(INPUT) == (1000*INPUT)

@then('dep_add returns our value + 1000')
def check_addition(dep_di):
    assert dep_di.dep_add(INPUT) == (1000+INPUT)

@then('dep_multiply mock returns 5000 * our value')
def check_mock_multiplication(dep_di_mock):
    assert dep_di_mock.dep_multiply(INPUT) == (5000*INPUT)

@then('dep_add mock returns our value + 5000')
def check_mock_addition(dep_di_mock):
    assert dep_di_mock.dep_add(INPUT) == (5000+INPUT)
