# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#       LOCAL BASE PATH
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set here only:
LOCAL_BASE_PATH = '/home/hsth/code/hughharford/nautilus/'
#                   "/home/hsth/code/hughharford/nautilus/"

# HIGH LEVEL CONFIGURATION OPTIONS:
####################################################
# ###################
# run using lean, expecting built containers etc
RUN_WITH_LEAN_CONTAINERS = True
RUN_VERBOSE_FOR_DEBUG = True # mostly leave this as true, update line above

highlevel_config_dict = {
    'RUN_WITH_LEAN_CONTAINERS': RUN_WITH_LEAN_CONTAINERS,
    'RUN_VERBOSE_FOR_DEBUG': RUN_VERBOSE_FOR_DEBUG,
}

# ################################## ##################################
#           MAIN NAUTILUS PARAMS
# ################################## ##################################

#                                   "condorgp/condorgp/util/logs"
NAUT_LOG_FILE = LOCAL_BASE_PATH + 'condorgp/condorgp/util/logs/nautilus_log.txt'
naut_dict = {
    'NAUT_LOG_FILE': NAUT_LOG_FILE,
}

# ################################## ##################################
#           MAIN LEAN PARAMS
# ################################## ##################################

LEAN_BASE_PATH = LOCAL_BASE_PATH + 'Lean/'
LOCALPACKAGES_PATH = LEAN_BASE_PATH + 'LocalPackages/condorgp/'
CONDORGP_PATH = LOCAL_BASE_PATH + 'condorgp/'
GP_CONDORGP_PATH = CONDORGP_PATH + 'condorgp/gp/'

LEAN_ALGOS_DIR = LEAN_BASE_PATH + 'Algorithm.Python/'
LEAN_LAUNCHER_DIR = 'Launcher/bin/Debug/'

LOCALPACKAGES_BACKTEST_OUTPUTS_DIR = LOCALPACKAGES_PATH + 'backtests/'

# outputs here:
LEAN_RESULTS_DIR = LOCALPACKAGES_BACKTEST_OUTPUTS_DIR

LEAN_CONFIG_DIR = LEAN_BASE_PATH + LEAN_LAUNCHER_DIR
LEAN_CONFIG_FILE = 'config.json'

CONDOR_CONFIG_FILE = 'config_condor.json'
CONDOR_CONFIG_PATH = 'leanQC/config/'
# /home/hsth/code/hughharford/condorgp/leanQC/config/config_test_algos_2.json

BACKTEST_LOG_LOCALPACKAGES = LOCALPACKAGES_BACKTEST_OUTPUTS_DIR + 'log.txt'

FITNESS_BASE = 'STATISTICS:: '
CURRENT_FITNESS_STAT = 'Return Over Maximum Drawdown'
FITNESS_CRITERIA = FITNESS_BASE + CURRENT_FITNESS_STAT

LEAN_TO_INJECT_TEMPLATE_ALGO = 'gpInjectAlgo.py'
LEAN_INJECTED_ALGO = 'gpInjectAlgo_done.py'
LEAN_INJECTED_ALGO_JSON = 'config_test_algos_gpInjectAlgo.json'



lean_dict = {
    'LEAN_CONFIG_FILE': LEAN_CONFIG_FILE,
    'LEAN_CONFIG_DIR': LEAN_CONFIG_DIR,
    'CONDOR_CONFIG_PATH': CONDOR_CONFIG_PATH,

    'CONDORGP_PATH': CONDORGP_PATH,
    'GP_CONDORGP_PATH': GP_CONDORGP_PATH,

    'LEAN_LAUNCHER_DIR': LEAN_LAUNCHER_DIR,
    'LEAN_ALGOS_FOLDER': LEAN_ALGOS_DIR,

    'LEAN_RESULTS_FOLDER': LEAN_RESULTS_DIR,

    'BACKTEST_LOG_LOCALPACKAGES': BACKTEST_LOG_LOCALPACKAGES,
    'LOCALPACKAGES_PATH': LOCALPACKAGES_PATH,

    'FITNESS_CRITERIA': FITNESS_CRITERIA,

    'LEAN_TO_INJECT_TEMPLATE_ALGO': LEAN_TO_INJECT_TEMPLATE_ALGO,
    'LEAN_INJECTED_ALGO': LEAN_INJECTED_ALGO,
    'LEAN_INJECTED_ALGO_JSON': LEAN_INJECTED_ALGO_JSON,

    }

# ################################## ##################################
#           TESTING PARAMS
# ################################## ##################################

CONDOR_TEST_CONFIG_FILE = 'config_test_condor.json'

CONDOR_TEST_CONFIG_FILE = 'config_test_condor.json'
CONDOR_TEST_CONFIG_FILE_1 = 'config_test_algos_1.json'
CONDOR_TEST_CONFIG_FILE_2 = 'config_test_algos_2.json'

BASIC_TEST_ALGO_NAME = 'IndBasicAlgo0.py'
CONFIG_TEST_ALGOS_FILE_1 = 'IndBasicAlgo1.py'
CONFIG_TEST_ALGOS_FILE_2 = 'IndBasicAlgo2.py'
BASIC_TEST_ALGO_LEAN = 'BasicTemplateFrameworkAlgorithm.py'


CONDOR_TEST_ALGOS_DIR = 'leanQC/config/'

CONDORGP_WITHIN_LEAN_DIR = LEAN_BASE_PATH + 'LocalPackages/condorgp/'
CONDORGP_IN_BACKTESTS_DIR = LEAN_BASE_PATH + 'LocalPackages/condorgp/backtests/'


test_dict = {
    'REASONABLE_FITNESS_SECS': 60,
    'CONDOR_TEST_ALGOS_FOLDER': CONDOR_TEST_ALGOS_DIR,

    'BASIC_TEST_ALGO_NAME': BASIC_TEST_ALGO_NAME,
    'CONFIG_TEST_ALGOS_FILE_1': CONFIG_TEST_ALGOS_FILE_1,
    'CONFIG_TEST_ALGOS_FILE_2': CONFIG_TEST_ALGOS_FILE_2,
    'BASIC_TEST_ALGO_LEAN': BASIC_TEST_ALGO_LEAN,

    'CONDOR_TEST_CONFIG_FILE': CONDOR_TEST_CONFIG_FILE,
    'CONDOR_TEST_CONFIG_FILE_1': CONDOR_TEST_CONFIG_FILE_1,
    'CONDOR_TEST_CONFIG_FILE_2': CONDOR_TEST_CONFIG_FILE_2,

    'CONDOR_CONFIG_PATH': CONDOR_CONFIG_PATH,

    'CONDORGP_WITHIN_LEAN_DIR': CONDORGP_WITHIN_LEAN_DIR,
    'CONDORGP_IN_BACKTESTS_DIR': CONDORGP_IN_BACKTESTS_DIR,

    }

# ################################## ##################################
#           UTIL PARAMS
# ################################## ##################################

NO_LOG_LINES = 300
CONDOR_LOG = LOCAL_BASE_PATH + 'condorgp/condorgp/util/logs/condor_log.txt'

util_dict = {
    'NO_LOG_LINES': NO_LOG_LINES,
    'CONDOR_LOG': CONDOR_LOG,
}
