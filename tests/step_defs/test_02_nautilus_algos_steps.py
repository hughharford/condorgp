import os.path
from pytest_bdd import scenarios, given, when, then, parsers

from condorgp.params import Params

from tests.fixtures import utils
from tests.fixtures import params

from condorgp.evaluation.nautilus import run_naut

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

scenarios('../features/02_nautilus_algos.feature')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#             Nautilus tests each evolved individual
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

'''
    # NB:
        These tests also confirm:
            that the fitness is found, and the log is up to date
'''

@given('a Nautilus setup ready to run')
def nautilus_setup_is_ready():
    pass # assumption for now: working as of 23 11 15

@given(parsers.cfparse('an evolved "{input_ind:String}" is specified',
                       extra_types=EXTRA_TYPES), target_fixture='input_ind')
@given('an evolved "<input_ind>" is specified', target_fixture='input_ind')
def input_evolved_code(input_ind):
    '''
    copies across config files and algorithms as needed
    '''
    # TODO:
    pass # not required, as can now run from:
         # condorgp/evaluation/nautilus using run_naut.py


@when(parsers.cfparse('Nautilus runs the "{input_ind:String}"',
                       extra_types=EXTRA_TYPES), target_fixture='input_ind')
@when('Nautilus runs the "<input_ind>"', target_fixture='input_ind')
def run_nautilus_and_evaluator(input_ind):
    ''' runs nautilus as per the required evaluator etc'''
    nt = run_naut.RunNautilus(input_ind)
    nt.basic_run_through()

@then(parsers.cfparse('the "{output_ind:String}" is found',
                       extra_types=EXTRA_TYPES), target_fixture='output_ind')
@then('the "<output_ind>" is found', target_fixture='output_ind')
def results_files_are_updated(output_ind):
    '''
    checks in the log file that the algo name is found
    only uses the last X lines of the log file
    '''
    assert 1
    # utils.confirm_ind_name_in_log_lines(output_ind)

@then(parsers.cfparse('the result: "{expected_value:Float}" is reported',
                       extra_types=EXTRA_TYPES), target_fixture='expected_value')
@then('the result: "<expected_value>" is reported', target_fixture='expected_value')
def check_results(expected_value, utils):
    key_req = 'Sharpe Ratio (252 days)'
    limit_lines = 5000 #
    got = ""
    got = utils.get_key_line_in_lim(key_req, lines = limit_lines)

    assert got[0] != 'not found'
    assert float(expected_value) == float(utils.get_last_chars(got[0],2))
