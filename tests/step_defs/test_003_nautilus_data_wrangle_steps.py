import os
import os.path

import pytest
import logging
from pytest_bdd import scenarios, given, when, then, parsers

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

"""
# wrangle data into bars
  Scenario Outline: When a csv of binance data is ready
    Given no bar Nautilus objects
    When a data wrangle is run
    Then an object of type XXX is added

# wrangled data is correctly formatted
  Scenario Outline: Binance wrangled data format works
    Given a bar Nautilus object
    When formatting is checked
    Then the bar formatting fits
"""


@given('no bar Nautilus objects')
def g_no_bar_nautilus_objects(cgp_data_objects=None):
    assert cgp_data_objects

@given('a bar Nautilus object')
def g_a_bar_Nautilus_object():
    assert 1

@when('a data wrangle is run')
def w_a_data_wrangel_is_run():
    assert 1

@when('formatting is checked')
def w_formatting_is_checked():
    assert 1

@then('an object of type XXX is added')
def t_an_object_of_type_XXX_is_added():
    assert 1

@then('the bar formatting fits')
def t_the_bar_formatting_fits():
    assert 1
