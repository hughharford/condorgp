from condorgp.params import Params
from condorgp.util.utils import Utils
from condorgp.util.log import CondorLogger
import logging

class GpFunctions():
    '''
    Support functions for gp activities.
    '''

    def __init__(self):
        self.util = Utils()
        # self.log = CondorLogger().get_logger()

        p = Params()
        self.util_dict = p.get_params("util_dict")
        self.test_dict = p.get_params("test_dict")
        self.naut_dict = p.get_params("naut_dict")

    def print_out_please(self):
        print(f'{"print_out_please___"*5}')

    def get_fit_nautilus_1(self):
        f = 0.0
        lines_to_check = 1500
        log_file = self.naut_dict['NAUTILUS_LOG_FILE'] # check Nautilus log!

        latest_log = self.util.get_last_x_log_lines(lines = lines_to_check,
                                                    log_file_n_path = log_file)
        if latest_log:
            # if no errors, retrieve fitness
            fitness_line = self.naut_dict['FITNESS_CRITERIA']
            lim = lines_to_check - 1
            got = self.util.get_key_line_in_lim(key = fitness_line,
                                                log_filepath = log_file,
                                                lines = lim)
            f = float(self.util.get_last_chars(got[0], ignore_last_chars = 4))
            logging.debug(f'<<< gpf.get_fit_nautilus_1 fitness = {f}, from {log_file}')
        else:
            f = -8888.8 # no backtest folder found
            logging.warning(f'<<< gpf.get_fit_nautilus_1 fitness {f}, no file/folder found @ {log_file}')
        if f > 50:
            f = -1111.1 # set low if unrealistic!
            logging.warning(f'<<< gpf.get_fit_nautilus_1 fitness = {f}, as > 50 and unrealistic')
        return f

if __name__ == "__main__":
    gpf = GpFunctions()
    print(gpf.get_fit_nautilus_1())
