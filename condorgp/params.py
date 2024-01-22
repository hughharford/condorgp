# params class defined here to hold dicts of parameter values

class Params():
    '''
    To hold all the parameters needed, and master them.

    Util (util_dict), Test (test_dict)
    Nautilus (naut_dict), High Level Config (highlevelconfig_dict)
    '''

    def __init__(self):
        self.params_list = []
        self.collect_params()
        self.add_dict_params(self.util_dict)
        self.add_dict_params(self.naut_dict)
        self.add_dict_params(self.test_dict)
        self.add_dict_params(self.highlevel_config_dict)

    def add_dict_params(self, params_dict):
        self.params_list.append(params_dict)

    def get_num_params(self):
        return len(self.params_list)

    def get_params_list(self):
        return self.params_list

    def get_params(self, requested_params = ""):
        if requested_params == "": return 1
        elif requested_params == "util_dict":
            return self.util_dict
        elif requested_params == "test_dict":
            return self.test_dict
        elif requested_params == "naut_dict":
            return self.naut_dict
        elif requested_params == "highlevel_config_dict":
            return self.highlevel_config_dict

    def collect_params(self):
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #       LOCAL BASE PATH
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Set here only:
        LOCAL_BASE_PATH = '/home/hughharford/code/hughharford/condorgp/'

        # HIGH LEVEL CONFIGURATION OPTIONS:
        ####################################################
        # ###################
        RUN_VERBOSE_FOR_DEBUG = False

        self.highlevel_config_dict = {
            'RUN_VERBOSE_FOR_DEBUG': RUN_VERBOSE_FOR_DEBUG,
            'LOCAL_BASE_PATH': LOCAL_BASE_PATH,
        }

        # ################################## ##################################
        #           MAIN NAUTILUS PARAMS
        # ################################## ##################################

        NAUTILUS_BASE_PATH = '/home/hughharford/code/hughharford/nautilus_trader/'
        NAUTILUS_EVAL_PATH = LOCAL_BASE_PATH + "condorgp/evaluation/"
        NAUTILUS_LOG_FILE = LOCAL_BASE_PATH + 'condorgp/util/logs/nautilus_log.json'
        CONDOR_LOG_FILE = LOCAL_BASE_PATH + 'condorgp/util/logs/condor_log.txt'
        LOGS_FOLDER = 'condorgp/util/logs/'
        CHECKPOINT_PATH = LOCAL_BASE_PATH + "condorgp/util/checkpoints/"
        RUN_DONE_TEXT = "done"
        NUM_LOG_BACKUPS = 3
        FITNESS_CRITERIA = 'Sharpe Ratio (252 days)'
        SIMPLE_FITNESS_CRITERIA = 'Risk Return Ratio'
        CGP_NAUT_STRATEGIES = NAUTILUS_EVAL_PATH + "cgp_naut_strategies.py"
        NAUT_DEFAULT_RUNNER = "naut_03_egFX.py"
        N_DEFAULT_RUN_INC_PATH = NAUTILUS_EVAL_PATH + NAUT_DEFAULT_RUNNER
        VERBOSITY = RUN_VERBOSE_FOR_DEBUG
        ELITE_NO = 1

        self.naut_dict = {
            'VERBOSITY': VERBOSITY,
            'NAUTILUS_BASE_PATH': NAUTILUS_BASE_PATH,
            'NAUTILUS_EVAL_PATH': NAUTILUS_EVAL_PATH,
            'LOGS_FOLDER': LOGS_FOLDER,
            'NUM_LOG_BACKUPS': NUM_LOG_BACKUPS,
            'NAUTILUS_LOG_FILE': NAUTILUS_LOG_FILE,
            'CONDOR_LOG_FILE': CONDOR_LOG_FILE,
            'CHECKPOINT_PATH': CHECKPOINT_PATH,
            'RUN_DONE_TEXT': RUN_DONE_TEXT,
            'FITNESS_CRITERIA': FITNESS_CRITERIA,
            'SIMPLE_FITNESS_CRITERIA': SIMPLE_FITNESS_CRITERIA,
            'CGP_NAUT_STRATEGIES': CGP_NAUT_STRATEGIES,
            'NAUT_DEFAULT_RUNNER': NAUT_DEFAULT_RUNNER,
            'N_DEFAULT_RUN_INC_PATH': N_DEFAULT_RUN_INC_PATH,
            'ELITE_NO': ELITE_NO,
        }

        # ################################## ##################################
        #           TESTING PARAMS
        # ################################## ##################################

        CGP_TEST_PATH = LOCAL_BASE_PATH + "tests/"
        NAUTILUS_TEST_DATA_PATH = NAUTILUS_BASE_PATH + 'tests/test_data/'
        CGP_TEST_DATA = CGP_TEST_PATH + 'test_data/'

        self.test_dict = {
            'REASONABLE_FITNESS_SECS': 60,

            'CGP_TEST_PATH': CGP_TEST_PATH,
            'NAUTILUS_TEST_DATA_PATH': NAUTILUS_TEST_DATA_PATH,
            'CGP_TEST_DATA': CGP_TEST_DATA,
            }

        # ################################## ##################################
        #           UTIL PARAMS
        # ################################## ##################################

        NO_LOG_LINES = 2000

        self.util_dict = {
            'LOCAL_BASE_PATH': LOCAL_BASE_PATH,
            'NO_LOG_LINES': NO_LOG_LINES,
        }
