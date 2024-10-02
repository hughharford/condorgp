import os.path
import pytest
import logging
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
}

CONVERTERS = {
    'initial': int,
    'some': int,
    'total': int,
}

scenarios('../features/003_nautilus_data_wrangle.feature')

# SCENARIO 1
"""
# wrangle data into bars
  Scenario Outline: When a csv of binance data is ready
    Given no bar Nautilus objects
    When a data wrangle is run
    Then an object of type XXX is added
"""

# Fixture for the data factory
@pytest.fixture
def nautilus_raw():
    return DataFactory().nautilus_raw()

@given('no bar Nautilus objects')
def g_no_bar_nautilus_objects(nautilus_raw): # cgp_data_objs=None
    assert nautilus_raw
    if nautilus_raw:
        logging.debug(f"test_003: data objects X {nautilus_raw.get_no_objs}")


@when('a data wrangle is run')
def w_a_data_wrangel_is_run():
    assert 1


@then('an object of type XXX is added')
def t_an_object_of_type_XXX_is_added():
    assert 1

# SCENARIO 2
"""
# wrangled data is correctly formatted
  Scenario Outline: Binance wrangled data format works
    Given a bar Nautilus object
    When formatting is checked
    Then the bar formatting fits
"""

@given('a bar Nautilus object')
def g_a_bar_Nautilus_object():
    assert type()

@when('formatting is checked')
def w_formatting_is_checked():
    assert 1

@then('the bar formatting fits')
def t_the_bar_formatting_fits():
    assert 1
