import logging
import sys
from condorgp.params import Params


loggers = {}


import logging
from contextlib import redirect_stdout

import traceback


class CondorLogger:
    '''
        home grown logging, see examples below
    '''
    def get_logger(self):
        return self.log

    def __init__(self):
        p = Params()
        self.util_dict = p.get_params("util_dict")
        self.test_dict = p.get_params("test_dict")
        self.naut_dict = p.get_params("naut_dict")

        # this captures to file the Condor logs
        sys.stdout = open(self.naut_dict['CONDOR_LOG_FILE'], "a")
        e_type, e_val, e_tb = sys.exc_info()
        traceback.print_exception(e_type, e_val, e_tb, file = sys.stdout)

        # looking to get the Nautilus logs also to a file...
        sys.stderr = open(self.naut_dict['NAUTILUS_LOG_FILE'], "a")
        e_type, e_val, e_tb = sys.exc_info()
        traceback.print_exception(e_type, e_val, e_tb, file = sys.stderr)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        self.log = logging.getLogger()
        self.log.setLevel(logging.DEBUG)

        out = logging.StreamHandler(sys.stdout)
        out.setLevel(logging.DEBUG)
        out.setFormatter(formatter)
        self.log.addHandler(out)

        err = logging.StreamHandler(sys.stderr)
        err.setLevel(logging.DEBUG)
        err.setFormatter(formatter)
        self.log.addHandler(err)

        # consoleHandler = logging.StreamHandler()
        # self.log.addHandler(consoleHandler)



        # self.log = logging.getLogger()
        # self.log.setLevel(logging.DEBUG)
        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> TEST >>>>>>>>>>>>> ")
        # for m in self.log.handlers:
        #     print(m.get_name())

        # # # remove extant loggers
        # # # self.log = logging.getLogger('BACKTESTER-001') #.setLevel(logging.CRITICAL)
        # # theirlogger = logging.getLogger('BACKTESTER-001')
        # # # did not yield any handlers:
        # # #                           # nautilus_trader
        # # for l in theirlogger.handlers:
        # #     print("Their logger handler: " & str(l.get_name()))

        # #     # theirlogger.removeHandler(l)

        # # # logging.getLogger('BACKTESTER-001').setLevel(logging.INFO)


        # formatter = logging.Formatter('%(asctime)s -  %(levelname)s - %(message)s')

        # # further log levels for diff)erent handlers - so far to match:
        # # matching_level = logging.INFO # higher (less info): INFO
        # # REPLACED BY: self.log.level USE THIS INSTEAD
        # matching_level = self.log.level

        # # create console handler and set level
        # sh_out = logging.StreamHandler(stream=sys.stdout)
        # sh_out.setFormatter(formatter)
        # sh_out.setLevel(level=matching_level)

        # sh_err = logging.StreamHandler(stream=sys.stderr)
        # sh_err.setFormatter(formatter)
        # sh_err.setLevel(level=matching_level)

        # # set basic file handler
        # fh = logging.FileHandler(filename = util_dict['CONDOR_LOG'],
        #                         mode='a',
        #                         encoding=None,
        #                         delay=False,
        #                         )
        # fh.setFormatter(formatter)
        # fh.setLevel(level=matching_level)

        # # consoleHandler = logging.StreamHandler()
        # # self.log.addHandler(consoleHandler)

        # # add handlers to logger
        # self.log.addHandler(sh_out)
        # self.log.addHandler(sh_err)
        # self.log.addHandler(fh)
