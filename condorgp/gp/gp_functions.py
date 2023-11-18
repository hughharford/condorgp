from condorgp.params import Params
from condorgp.util.utils import Utils
from condorgp.util.log import CondorLogger


class GpFunctions():
    '''
    Support functions for gp activities.
    '''

    def __init__(self):
        self.util = Utils()
        self.log = CondorLogger().get_logger()

        p = Params()
        self.util_dict = p.get_params("util_dict")
        self.test_dict = p.get_params("test_dict")
        self.naut_dict = p.get_params("naut_dict")

    def print_out_please(self):
        print(f'{"print_out_please___"*5}')

    def get_fit_6(self):
        f = 0.0
        # find latest log, open log file
        latest_log = self.util.get_latest_log_content()
        log = self.util.get_log_filepath()
        if latest_log:
            cgp_error_mark = '<< CONDOR INJECT-CODE ERROR >>' # check for error
            for line in latest_log:
                if cgp_error_mark in line:
                    self.log.warn(f'<<< gpf.get_fit_6: inject error')
                    return -9999.9

            # if no errors, retrieve fitness
            RoMDD_line = 'STATISTICS:: Return Over Maximum Drawdown'
            lim = 10000
            got = self.util.get_key_line_in_lim(key = RoMDD_line,
                                                log_filepath = log,
                                                lines = lim)
            f = float(self.util.get_last_chars(got[0]))
            self.log.debug(f'<<< gpf.get_fit_6 fitness = {f}, from {log}')
        else:
            f = -8888.8 # no backtest folder found
            self.log.warn(f'<<< gpf.get_fit_6 fitness {f}, no folder found')
        if f > 1_000_000:
            f = -1111.1 # set low if actually 7.922e28!
            self.log.warn(f'<<< gpf.get_fit_6 fitness = {f}, as 7.922e28!')
        return f

    def get_fit_nautilus_1(self):
        # self.log.info(f'<<< RUNNING gpf.get_fit_nautilus_1')
        f = 0.0
        lines_to_check = 1500
        log_file = self.naut_dict['NAUTILUS_LOG_FILE'] # check the Nautilus log!

        latest_log = self.util.get_last_x_log_lines(lines = lines_to_check,
                                                    log_file_n_path = log_file)
        if latest_log:
            cgp_error_mark = '<< CONDOR INJECT-CODE ERROR >>' # check for error
            for line in latest_log:
                if cgp_error_mark in line:
                    self.log.warn(f'<<< gpf.get_fit_nautilus_1: inject error')
                    return -9999.9

            # if no errors, retrieve fitness
            RoMDD_line = 'Risk Return Ratio: '
            lim = lines_to_check - 1
            got = self.util.get_key_line_in_lim(key = RoMDD_line,
                                                log_filepath = log_file,
                                                lines = lim)
            f = float(self.util.get_last_chars(got[0], ignore_last_chars = 4))
            self.log.debug(f'<<< gpf.get_fit_nautilus_1 fitness = {f}, from {log_file}')
        else:
            f = -8888.8 # no backtest folder found
            self.log.warn(f'<<< gpf.get_fit_nautilus_1 fitness {f}, no folder found')
        if f > 50:
            f = -1111.1 # set low if unrealistic!
            self.log.warn(f'<<< gpf.get_fit_nautilus_1 fitness = {f}, as > 50 and unrealistic')
        return f

if __name__ == "__main__":
    gpf = GpFunctions()
    gpf.get_fit_nautilus_1()
