import os
import os.path

import pytest
from pytest_bdd import scenarios, given, when, then, parsers
import logging

from gp_fixtures import gp_control

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

pytest.foundfitness = 99

scenarios('../../features/up/004_deap_runs_nautilus.feature')


@given('a setup with Deap using Nautilus')
def setup_ready():
    ''' assumed setup ready '''
    pass # assumed, nothing operates otherwise

@when('a short Deap run is conducted')
def short_deap_run(gp_control):
    ''' shortest deap run possible '''
    assert gp_control is not None
    pset_used = 'naut_pset_01' # 'test_pset5c'
    newpop = 1
    gens = 1

    cp_freq = 0
    gp_control.set_gp_n_cp(freq=cp_freq, cp_file="empty")

    gp_control.setup_gp(pset_used, newpop, gens)
    gp_control.initiate_gp_run()

@then(parsers.cfparse('the result is not "{not_found_code:Float}"',
                       extra_types=EXTRA_TYPES), target_fixture='not_found_code')
@then('the result is not "<not_found_code>"')
def find_results(not_found_code, gp_control):
    ''' check getting anything but not found '''
    max_fitness_found = gp_control.gp.logbook.select("max")[-1]
    pytest.foundfitness = max_fitness_found
    assert not_found_code != max_fitness_found

@then(parsers.cfparse('the result is neither "{nan_code:Float}"',
                       extra_types=EXTRA_TYPES), target_fixture='nan_code')
@then('the result is neither "<nan_code>"')
def find_results(nan_code):
    ''' check getting anything but nan '''
    assert nan_code != pytest.foundfitness
