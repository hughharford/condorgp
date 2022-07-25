# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#       LOCAL BASE PATH
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set here only, in theory:
LOCAL_BASE_PATH = '/home/hsth/code/hughharford/'

# HIGH LEVEL CONFIGURATION OPTIONS:
####################################################
# ###################
# run using lean, expecting built containers etc
RUN_WITH_LEAN_CONTAINERS = False
RUN_VERBOSE_FOR_DEBUG = True # leave this as true, update the line above T/F

highlevel_config_dict = {
    'RUN_WITH_LEAN_CONTAINERS': RUN_WITH_LEAN_CONTAINERS,
    'RUN_VERBOSE_FOR_DEBUG': RUN_VERBOSE_FOR_DEBUG,
}


# ################################## ##################################
#           MAIN LEAN PARAMS
# ################################## ##################################

LEAN_BASE_PATH = LOCAL_BASE_PATH + 'Lean/'

LEAN_ALGOS_DIR = LEAN_BASE_PATH + 'Algorithm.Python/'
LEAN_LAUNCHER_DIR = 'Launcher/bin/Debug/'

LEAN_BACKTEST_OUTPUTS_DIR = LEAN_BASE_PATH + 'Backtests/'
# outputs here:
LEAN_RESULTS_DIR = LEAN_BACKTEST_OUTPUTS_DIR

LEAN_CONFIG_DIR = LEAN_BASE_PATH + LEAN_LAUNCHER_DIR
LEAN_CONFIG_FILE = 'config.json'

CONDOR_CONFIG_FILE = 'config_condor.json'
CONDOR_CONFIG_PATH = 'leanQC/config/'
# /home/hsth/code/hughharford/condorgp/leanQC/config/config_test_algos_2.json

BACKTEST_LOG = LEAN_BACKTEST_OUTPUTS_DIR + 'log.txt'

FITNESS_BASE = 'STATISTICS:: '
CURRENT_FITNESS_STAT = 'Return Over Maximum Drawdown'
FITNESS_CRITERIA = FITNESS_BASE + CURRENT_FITNESS_STAT

ALGO_WRAPPER_SIN_PY = 'gpInjectAlgo'

lean_dict = {
    'LEAN_CONFIG_FILE': LEAN_CONFIG_FILE,
    'LEAN_CONFIG_DIR': LEAN_CONFIG_DIR,

    'LEAN_LAUNCHER_DIR': LEAN_LAUNCHER_DIR,
    'LEAN_ALGOS_FOLDER': LEAN_ALGOS_DIR,

    'LEAN_RESULTS_FOLDER': LEAN_RESULTS_DIR,
    'LEAN_BACKTEST_OUTPUTS_DIR': LEAN_BACKTEST_OUTPUTS_DIR,

    'BACKTEST_LOG': BACKTEST_LOG,

    'FITNESS_CRITERIA': FITNESS_CRITERIA,

    'ALGO_WRAPPER_SIN_PY': ALGO_WRAPPER_SIN_PY,

    }

# ################################## ##################################
#           TESTING PARAMS
# ################################## ##################################

CONDOR_TEST_CONFIG_FILE = 'config_test_condor.json'

CONFIG_TEST_ALGOS_FILE_1 = 'config_test_algos_1.json'
CONFIG_TEST_ALGOS_FILE_2 = 'config_test_algos_2.json'

BASIC_TEST_ALGO_NAME = 'IndBasicAlgo1'

CONDOR_TEST_ALGOS_DIR = 'leanQC/config/'

CONDORGP_WITHIN_LEAN_DIR = LEAN_BASE_PATH + 'LocalPackages/condorgp/'
CONDORGP_IN_BACKTESTS_DIR = '/home/hsth/code/hughharford/Lean/LocalPackages/condorgp/backtests/'

test_dict = {
    'REASONABLE_FITNESS_SECS': 60,
    'CONDOR_TEST_ALGOS_FOLDER': CONDOR_TEST_ALGOS_DIR,

    'CONFIG_TEST_ALGOS_FILE_1': CONFIG_TEST_ALGOS_FILE_1,
    'CONFIG_TEST_ALGOS_FILE_2': CONFIG_TEST_ALGOS_FILE_2,
    'CONDOR_TEST_CONFIG_FILE': CONDOR_TEST_CONFIG_FILE,

    'BASIC_TEST_ALGO_NAME': BASIC_TEST_ALGO_NAME,

    'CONDOR_CONFIG_PATH': CONDOR_CONFIG_PATH,

    'CONDORGP_WITHIN_LEAN_DIR': CONDORGP_WITHIN_LEAN_DIR,
    'CONDORGP_IN_BACKTESTS_DIR': CONDORGP_IN_BACKTESTS_DIR
    }

# ################################## ##################################
#           UTIL PARAMS
# ################################## ##################################

NO_LOG_LINES = 150
CONDOR_BASE_PATH = LOCAL_BASE_PATH + 'condorgp/'
CONDOR_LOG_PATH = CONDOR_BASE_PATH + 'condorgp/util/logs/'
CONDOR_LOG = CONDOR_LOG_PATH + 'condor_log.txt'

util_dict = {
    'CONDOR_LOG_PATH': CONDOR_LOG_PATH,
    'CONDOR_LOG': CONDOR_LOG,
    'NO_LOG_LINES': NO_LOG_LINES,

}
