import pytest
from pytest_bdd import scenarios, given, when, then, parsers

from condorgp.factories.data_factory import DataFactory

''' FEATURE DESCRIPTION:
Feature: CondorGp's evolutions need fitness checking against data
  As a gp algorithm reliant on data,
  Data must be found, wrangled and correctly available
  To allow backtesting.
'''

EXTRA_TYPES = {
    'Number': int,
    'String': str,
    'Float': float,
    'nautilus_bar': str,
}

CONVERTERS = {
    'initial': int,
    'some': int,
    'total': int,
}

scenarios('../features/015_microk8s_start.feature')

# ----------------------------------------------
# Fixtures
# ----------------------------------------------
@pytest.fixture
def nautilus_raw():
    return DataFactory().nautilus_raw()

# ----------------------------------------------
# pytest-BDD hooks
# ----------------------------------------------
@pytest.hookimpl
def pytest_bdd_before_scenario(request, feature, scenario):
    print("Before scenario:", scenario.name)
    # Perform setup actions
    nautilus_raw.show_expectations()
    nautilus_raw.setup_catalog()
    # Access scenario-specific information via the 'scenario' argument

@pytest.hookimpl
def pytest_bdd_after_scenario(request, feature, scenario, result):
    print("After scenario:", scenario.name)
    # Perform cleanup actions
    # Access scenario-specific information via the 'scenario' argument


@given('a bar Nautilus object in a catalog')
def g_a_bar_Nautilus_object_in_a_catalog(nautilus_raw):
    assert 1 == 1

@when('formatting is checked')
def w_formatting_is_checked():
    assert 1

@then('the bar formatting fits')
def t_the_bar_formatting_fits():
    assert 1
