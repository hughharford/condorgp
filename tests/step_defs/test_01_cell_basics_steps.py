from pytest_bdd import scenarios, given, when, then, parsers

from condor_start.cell_runner import Cell

EXTRA_TYPES = {
    'Number': int,
    'String': str,
}

CONVERTERS = {
    'initial': int,
    'some': int,
    'total': int,
}

scenarios('../features/01_cell_basics.feature')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#             ADD CELLS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
Scenario Outline: Add cells
    Given the nest has "<initial>" cells
    When "<some>" cells are added to the nest
    Then the nest contains "<total>" cells
"""

@given(parsers.cfparse('the nest has "{initial:Number}" cells', extra_types=EXTRA_TYPES), target_fixture='cells')
@given('the next has "<initial>" cells', target_fixture='cells')
def cells_add(initial):
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

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#             REMOVE CELLS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
Scenario Outline: Remove cells
    Given the existing nest has "<initial>" cells
    When "<some>" cells are removed
    Then the nest now contains "<total>" cells
"""

@given(parsers.cfparse('the existing nest has "{initial:Number}" cells', extra_types=EXTRA_TYPES), target_fixture='cells')
@given('the existing nest has "<initial>" cells', target_fixture='cells')
def cells_remove(initial):
    # for i in range(12):
    #      Cell(f'dummy_ref1 {i}','PROTOTYPE')
    assert len(Cell.getcelllist()) == initial

@when(parsers.cfparse('"{some:Number}" cells are removed', extra_types=EXTRA_TYPES))
@when('"<some>"  cells are removed')
def when_somecellsareremoved(some):
    for i in range(some):
        Cell(f'dummy_ref1 {i}','PROTOTYPE')

@then(parsers.cfparse('the nest now contains "{total:Number}" cells', extra_types=EXTRA_TYPES))
@then('the nest now contains "<total>" cells')
def then_thecelllistisdecremented(total):
    assert len(Cell.getcelllist()) == total


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#             CELL ID CHANGE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
Scenario: Cell id change
    Given a pre-created cell with <initial_id>
    When the cell id is changed to <text_to_change_to>
    Then the new cell id is <intended_id>
"""

# @given(parsers.cfparse('the existing nest has "{initial_id:String}" cells', extra_types=EXTRA_TYPES), target_fixture='cells')
# @given('the existing nest has "<initial_id>" cells', target_fixture='cells')
# def cells(initial_id):
#     firstCell = Cell(initial_id) == initial_id
# @given('a pre-created cell')
# def given_aprecreatedcell():
#     pass

# @when('the cell id is changed')
# def when_thecellidischanged():
#     pass

# @then('the new cell id is as expected')
# def then_cellidisasexpected():
#     assert 'dark' == 'dark'
