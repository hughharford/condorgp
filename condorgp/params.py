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
        # run using lean, expecting built containers etc
        # TODO: Delete __ RUN_WITH_LEAN_CONTAINERS = True
        RUN_VERBOSE_FOR_DEBUG = True # mostly leave this as true, update line above

        self.highlevel_config_dict = {
            # TODO: Delete __ 'RUN_WITH_LEAN_CONTAINERS': RUN_WITH_LEAN_CONTAINERS,
            'RUN_VERBOSE_FOR_DEBUG': RUN_VERBOSE_FOR_DEBUG,
            'LOCAL_BASE_PATH': LOCAL_BASE_PATH,
        }

        # ################################## ##################################
        #           MAIN NAUTILUS PARAMS
        # ################################## ##################################

        # /home/hsth/code/hughharford/nautilus/condorgp/condorgp/util/logs/nautilus_log.txt

        #                                   "condorgp/condorgp/util/logs"
        NAUTILUS_EVALUATION_PATH = LOCAL_BASE_PATH + "condorgp/evaluation/nautilus/"
                                            # "condorgp/util/logs/nautilus_log.json"
        NAUTILUS_LOG_FILE = LOCAL_BASE_PATH + 'condorgp/util/logs/nautilus_log.json'
        CONDOR_LOG_FILE = LOCAL_BASE_PATH + 'condorgp/util/logs/condor_log.txt'
        LOGS_FOLDER = 'condorgp/util/logs/'
        FITNESS_CRITERIA = 'Sharpe Ratio (252 days)'

        self.naut_dict = {
            'NAUTILUS_EVALUATION_PATH': NAUTILUS_EVALUATION_PATH,
            'LOGS_FOLDER': LOGS_FOLDER,
            'NAUTILUS_LOG_FILE': NAUTILUS_LOG_FILE,
            'CONDOR_LOG_FILE': CONDOR_LOG_FILE,
            'FITNESS_CRITERIA': FITNESS_CRITERIA,
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


        self.test_dict = {
            'REASONABLE_FITNESS_SECS': 60,
            'CONDOR_TEST_ALGOS_FOLDER': CONDOR_TEST_ALGOS_DIR,

            'BASIC_TEST_ALGO_NAME': BASIC_TEST_ALGO_NAME,
            'CONFIG_TEST_ALGOS_FILE_1': CONFIG_TEST_ALGOS_FILE_1,
            'CONFIG_TEST_ALGOS_FILE_2': CONFIG_TEST_ALGOS_FILE_2,
            'BASIC_TEST_ALGO_LEAN': BASIC_TEST_ALGO_LEAN,

            'CONDOR_TEST_CONFIG_FILE': CONDOR_TEST_CONFIG_FILE,
            'CONDOR_TEST_CONFIG_FILE_1': CONDOR_TEST_CONFIG_FILE_1,
            'CONDOR_TEST_CONFIG_FILE_2': CONDOR_TEST_CONFIG_FILE_2,
            }

        # ################################## ##################################
        #           UTIL PARAMS
        # ################################## ##################################

        NO_LOG_LINES = 2000
        CONDOR_LOG = LOCAL_BASE_PATH + 'condorgp/condorgp/util/logs/condor_log.txt'

        self.util_dict = {
            'LOCAL_BASE_PATH': LOCAL_BASE_PATH,
            'NO_LOG_LINES': NO_LOG_LINES,
            'CONDOR_LOG': CONDOR_LOG,
        }
