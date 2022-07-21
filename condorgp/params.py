
# ################################## ##################################
#           MAIN LEAN PARAMS
# ################################## ##################################

LEAN_BASE_PATH = '/home/hsth/code/hughharford/Lean/'

LEAN_ALGOS_DIR = LEAN_BASE_PATH + 'Algorithm.Python/'
LEAN_LAUNCHER_DIR = 'Launcher/bin/Debug/'

LEAN_BACKTEST_OUTPUTS_DIR = LEAN_BASE_PATH + 'Backtests/'
# outputs here:
LEAN_RESULTS_DIR = LEAN_BACKTEST_OUTPUTS_DIR

LEAN_CONFIG_DIR = LEAN_BASE_PATH + LEAN_LAUNCHER_DIR
LEAN_CONFIG_FILE = 'config.json'

CONDOR_CONFIG_FILE = 'config_condor.json'
CONDOR_CONFIG_PATH = 'leanQC/config/'

BACKTEST_LOG_FILE_N_PATH = LEAN_BACKTEST_OUTPUTS_DIR + 'log.txt'

lean_dict = {
    'LEAN_CONFIG_FILE': LEAN_CONFIG_FILE,
    'LEAN_CONFIG_DIR': LEAN_CONFIG_DIR,

    'LEAN_LAUNCHER_DIR': LEAN_LAUNCHER_DIR,
    'LEAN_ALGOS_FOLDER': LEAN_ALGOS_DIR,

    'LEAN_RESULTS_FOLDER': LEAN_RESULTS_DIR,
    'LEAN_BACKTEST_OUTPUTS_DIR': LEAN_BACKTEST_OUTPUTS_DIR,

    'BACKTEST_LOG_FILE_N_PATH': BACKTEST_LOG_FILE_N_PATH,

    }

# ################################## ##################################
#           TESTING PARAMS
# ################################## ##################################

CONDOR_TEST_CONFIG_FILE = 'config_test_condor.json'

CONDOR_TEST_CONFIG_FILE_1 = 'config_test_condor_1.json'
CONDOR_TEST_CONFIG_FILE_2 = 'config_test_condor_2.json'

CONDOR_TEST_ALGOS_DIR = 'leanQC/config/'

test_dict = {
    'REASONABLE_FITNESS_SECS': 60,
    'CONDOR_TEST_ALGOS_FOLDER': CONDOR_TEST_ALGOS_DIR,

    'CONDOR_TEST_CONFIG_FILE_1': CONDOR_TEST_CONFIG_FILE_1,
    'CONDOR_TEST_CONFIG_FILE_2': CONDOR_TEST_CONFIG_FILE_2,
    'CONDOR_TEST_CONFIG_FILE': CONDOR_TEST_CONFIG_FILE,


    'CONDOR_CONFIG_PATH': CONDOR_CONFIG_PATH,
    }

# ################################## ##################################
#           UTIL PARAMS
# ################################## ##################################

NO_LOG_LINES = 150

util_dict = {
    'NO_LOG_LINES': NO_LOG_LINES
}
