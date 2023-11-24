import logging
import sys
from condorgp.params import Params

import traceback


class CondorLogger:
    '''
        home grown logging, see examples below
    '''
    def __init__(self):
        p = Params()
        self.util_dict = p.get_params("util_dict")
        self.test_dict = p.get_params("test_dict")
        self.naut_dict = p.get_params("naut_dict")

        # if hasattr(self, "log"):
        self.log = self.create_logger()

    def create_logger(self):
        loglevel = logging.INFO # logging.DEBUG # logging.INFO

        # this captures to file the Condor logs
        sys.stdout = open(self.naut_dict['CONDOR_LOG_FILE'], "a")
        e_type, e_val, e_tb = sys.exc_info()
        traceback.print_exception(e_type, e_val, e_tb, file = sys.stdout)

        # # looking to get the Nautilus logs also to a file...
        # sys.stderr = open(self.naut_dict['NAUTILUS_LOG_FILE'], "a")
        # e_type, e_val, e_tb = sys.exc_info()
        # traceback.print_exception(e_type, e_val, e_tb, file = sys.stderr)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        l = logging.getLogger()
        l.propagate = False
        l.setLevel(loglevel)

        out = logging.StreamHandler(sys.stdout)
        out.setLevel(loglevel)
        out.setFormatter(formatter)
        l.addHandler(out)

        err = logging.StreamHandler(sys.stderr)
        err.setLevel(loglevel)
        err.setFormatter(formatter)
        l.addHandler(err)

        return l

    def get_logger(self):
        return self.log
