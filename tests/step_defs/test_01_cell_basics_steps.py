from pytest_bdd import scenarios, given, when, then, parsers

from condor_start.cell_runner import Cell

EXTRA_TYPES = {
    'Number': int,
}


CONVERTERS = {
    'initial': int,
    'some': int,
    'total': int,
}

scenarios('../features/01_cell_basics.feature')
"""
    Scenario: Cell creation
    Given pre-created cells
    When another cell is created
    Then the celllist is incremented
"""

# the nest has "<initial>" cells
@given(parsers.cfparse('the nest has "{initial:Number}" cells', extra_types=EXTRA_TYPES), target_fixture='cells')
@given('the basket has "<initial>" cells', target_fixture='cells')
def cells(initial):
    assert len(Cell.getcelllist()) == initial

@when(parsers.cfparse('"{some:Number}" cells are added to the nest', extra_types=EXTRA_TYPES))
@when('"<some>"  cells are added to the nest')
def when_somecellsarecreated(some):
    for i in range(some):
        Cell(f'dummy_ref1 {i}','PROTOTYPE')

@then(parsers.cfparse('the nest contains "{total:Number}" cells', extra_types=EXTRA_TYPES))
@then('the nest contains "<total>" cells')
def then_thecelllistisincremented(total):
    assert len(Cell.getcelllist()) == total

# """
#     Scenario: Cell id
#     Given a pre-created cell
#     When the cell id is changed
#     Then the new cell id is as expected
# """

# @given('a pre-created cell')
# def given_aprecreatedcell():
#     pass

# @when('the cell id is changed')
# def when_thecellidischanged():
#     pass

# @then('the new cell id is as expected')
# def then_cellidisasexpected():
#     assert 'dark' == 'dark'
