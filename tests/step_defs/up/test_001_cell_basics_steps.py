from pytest_bdd import scenarios, given, when, then, parsers
import pytest

from cell_fixtures import cell, cells

EXTRA_TYPES = {
    'Number': int,
    'String': str,
}

CONVERTERS = {
    'initial': int,
    'some': int,
    'total': int,
}


scenarios('../../features/up/001_cell_basics.feature')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#             ADD CELLS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


@given(parsers.cfparse('the nest has "{initial:Number}" cells',
                       extra_types=EXTRA_TYPES))
@given('the next has "<initial>" cells', target_fixture='initial')
def cells_add(initial, cells):
    assert cells.get_cell_count() == initial

@when(parsers.cfparse('"{some:Number}" cells are added to the nest',
                      extra_types=EXTRA_TYPES))
@when('"<some>"  cells are added to the nest', target_fixture='some')
def when_some_cells_are_created(some, cells):
    for i in range(some):
        cells.new_cell(user_ref=f'dummy_ref1 {i}', celltype='PROTOTYPE')

@then(parsers.cfparse('the nest contains "{total:Number}" cells',
                      extra_types=EXTRA_TYPES))
@then('the nest contains "<total>" cells', target_fixture='total')
def then_the_cell_list_is_incremented(total, cells):
    assert cells.get_cell_count() == total

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#             REMOVE CELLS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


@given(parsers.cfparse('the existing nest has "{initial:Number}" cells',
                        extra_types=EXTRA_TYPES))
@given('the existing nest has "<initial>" cells')
def cells_remove(initial, cells):
    assert cells.get_cell_count() == initial

@when(parsers.cfparse('"{some:Number}" cells are removed',
                        extra_types=EXTRA_TYPES))
@when('"<some>"  cells are removed')
def when_some_cells_are_removed(some, cells):
    for i in range(some):
        cells.pop_cell()

@then(parsers.cfparse('the nest now contains "{total:Number}" cells'
                      , extra_types=EXTRA_TYPES))
@then('the nest now contains "<total>" cells')
def then_the_cell_list_has_been_decremented(total, cells):
    assert cells.get_cell_count()  == total


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#             CELL ID CHANGE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
