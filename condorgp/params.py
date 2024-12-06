# params class defined here to hold dicts of parameter values
import os
import logging, traceback

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
        # now need to set some options, based on os.environ["AMQP_URL"]
        LOCAL_BASE_PATH = '/home/hughharford/code/hughharford/condorgp/'
        try:
            # check = ''
            # if "AMQP_URL" in os.environ:
            #     check = os.environ["AMQP_URL"]
            # # if no error to checking the
            # # then on a container using RabbitMQ and thereby needs path below:
            #     if len(check) > 0:
            #         LOCAL_BASE_PATH = '/home/user/code/condorgp/'
            # if "IN_DOCKER" in os.environ:
            #     LOCAL_BASE_PATH = '/condorgp/'
            if os.environ['ON_PRIMARY'] == 1:
                LOCAL_BASE_PATH = '/home/hughharford/code/hughharford/condorgp/'

        except BaseException as e:
            logging.debug(f"CondorGP Params ERROR: {e}")
            tb = ''.join(traceback.format_tb(e.__traceback__))
            logging.debug(f"CondorGP Params : {tb}")


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

        FITNESS_CRITERIA_SHARPE_RATIO = 'Sharpe Ratio (252 days)'
        FITNESS_CRITERIA_RISK_RETURN_RATIO = 'Risk Return Ratio'
        FITNESS_CRITERIA_PNL_TOTAL = 'PnL (total)'
        FITNESS_CRITERIA_AVG_RETURN = 'Average (Return)'

        BACKTEST_ID_CURRENT = "BACKTESTER-001-naut-run-06"
        CGP_NAUT_STRATEGIES = NAUTILUS_EVAL_PATH + "cgp_naut_strategies.py"
        NAUT_DEFAULT_RUNNER = "naut_03_egFX.py"
        N_DEFAULT_RUN_INC_PATH = NAUTILUS_EVAL_PATH + NAUT_DEFAULT_RUNNER
        VERBOSITY = RUN_VERBOSE_FOR_DEBUG
        NO_OF_ELITE = 1 # make this 0 to remove elitism

        NAUT_DATA_PATH = LOCAL_BASE_PATH + 'data/'
        NAUT_RAW_DATA_PATH = LOCAL_BASE_PATH + 'raw_data/'


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

            'FITNESS_CRITERIA_SHARPE_RATIO': FITNESS_CRITERIA_SHARPE_RATIO,
            'FITNESS_CRITERIA_RISK_RETURN_RATIO': FITNESS_CRITERIA_RISK_RETURN_RATIO,
            'FITNESS_CRITERIA_PNL_TOTAL': FITNESS_CRITERIA_PNL_TOTAL,
            'FITNESS_CRITERIA_AVG_RETURN': FITNESS_CRITERIA_AVG_RETURN,

            'SPECIFIED_FITNESS': FITNESS_CRITERIA_SHARPE_RATIO,

            'BACKTEST_ID_CURRENT': BACKTEST_ID_CURRENT,
            'CGP_NAUT_STRATEGIES': CGP_NAUT_STRATEGIES,
            'NAUT_DEFAULT_RUNNER': NAUT_DEFAULT_RUNNER,
            'N_DEFAULT_RUN_INC_PATH': N_DEFAULT_RUN_INC_PATH,
            'NO_OF_ELITE': NO_OF_ELITE,

            'NAUT_DATA_PATH': NAUT_DATA_PATH, # wrangled nautilus data
            'NAUT_RAW_DATA_PATH': NAUT_RAW_DATA_PATH, # downloaded csv's etc
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
