from pytest_bdd import scenarios, given, when, then, parsers

from cell_fixtures import cell_central

EXTRA_TYPES = {
    'Number': int,
    'String': str,
}

CONVERTERS = {
    'initial': int,
    'some': int,
    'total': int,
}



scenarios('../../features/up/01_cell_basics.feature')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#             ADD CELLS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
Scenario Outline: Add cells
    Given the nest has "<initial>" cells
    When "<some>" cells are added to the nest
    Then the nest contains "<total>" cells
"""

@given(parsers.cfparse('the nest has "{initial:Number}" cells',
                       extra_types=EXTRA_TYPES), target_fixture='cells')
@given('the next has "<initial>" cells', target_fixture='cells')
def cells_add(initial, cell_central):
    assert len(cell_central.get_cell_list()) == initial

@when(parsers.cfparse('"{some:Number}" cells are added to the nest',
                      extra_types=EXTRA_TYPES))
@when('"<some>"  cells are added to the nest')
def when_some_cells_are_created(some, cell_central):
    for i in range(some):
        cell_central.new_cell(new_cell_ref=f'dummy_ref1 {i}', new_cell_type='PROTOTYPE')

@then(parsers.cfparse('the nest contains "{total:Number}" cells',
                      extra_types=EXTRA_TYPES))
@then('the nest contains "<total>" cells')
def then_the_cell_list_is_incremented(total, cell_central):
    assert len(cell_central.get_cell_list()) == total

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
def cells_remove(initial, cell_central):
    assert len(cell_central.get_cell_list()) == initial

@when(parsers.cfparse('"{some:Number}" cells are removed', extra_types=EXTRA_TYPES))
@when('"<some>"  cells are removed')
def when_some_cells_are_removed(some, cell_central):
    for i in range(some):
        cell_central.pop_random_cell()

@then(parsers.cfparse('the nest now contains "{total:Number}" cells', extra_types=EXTRA_TYPES))
@then('the nest now contains "<total>" cells')
def then_the_cell_list_has_been_decremented(total, cell_central):
    assert len(cell_central.get_cell_list()) == total


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
