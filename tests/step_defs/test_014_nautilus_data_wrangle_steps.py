import pytest
from pytest_bdd import scenarios, given, when, then, parsers

from condorgp.factories.data_factory import DataFactory

from nautilus_trader.persistence.catalog import ParquetDataCatalog

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

scenarios('../features/014_nautilus_data_wrangle.feature')

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

# SCENARIO 1
"""
# wrangle data into bars
  Scenario Outline: When a csv of binance data is ready
    Given no bar Nautilus objects
    When a data wrangle is run
    Then an object of type XXX is added
"""
@given('no bar Nautilus objects')
def g_no_bar_nautilus_objects(nautilus_raw): # cgp_data_objs=None
    assert nautilus_raw.get_no_objs() == 0

@when('a data wrangle is run')
def w_a_data_wrangel_is_run(nautilus_raw):
    before_count = nautilus_raw.get_no_objs()
    nautilus_raw.default_wrangle()
    after_count = nautilus_raw.get_no_objs()
    assert after_count != before_count
    assert after_count > before_count

@then('an object of type XXX is added')
def t_an_object_of_type_XXX_is_added():
    assert 1

# SCENARIO 2
"""
# wrangled data is correctly formatted
  Scenario Outline: Binance wrangled data format works
    Given a bar Nautilus object in a catalog
    When formatting is checked
    Then the bar formatting fits
"""

@given('a bar Nautilus object in a catalog')
def g_a_bar_Nautilus_object_in_a_catalog(nautilus_raw):
    assert type(nautilus_raw.get_default_catalog()) == ParquetDataCatalog

@when('formatting is checked')
def w_formatting_is_checked():
    assert 1

@then('the bar formatting fits')
def t_the_bar_formatting_fits():
    assert 1
