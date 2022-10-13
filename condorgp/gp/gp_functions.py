from condorgp.params import util_dict, test_dict, lean_dict
from condorgp.util.utils import Utils
from condorgp.util.log import CondorLogger


class GpFunctions:
    '''
    Support functions for gp activities.
    '''

    def __init__(self):
        self.util = Utils()
        self.log = CondorLogger().get_logger()

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
                    self.log.warn(f'<<< gpf.get_fitness_6: inject error')
                    return -9999.9

            # if no errors, retrieve fitness
            RoMDD_line = 'STATISTICS:: Return Over Maximum Drawdown'
            lim = 10000
            got = self.util.get_key_line_in_lim(key = RoMDD_line,
                                                log_filepath = log,
                                                limit_lines = lim)
            f = float(self.util.get_last_chars(got[0]))
            self.log.debug(f'<<< gpf.get_fitness_6 fitness = {f}, from {log}')
            # get_fitness_6
        else:
            f = -8888.8 # no backtest folder found
            self.log.warn(f'<<< gpf.get_fitness_6 fitness {f}, no folder found')
        return f

if __name__ == "__main__":
    gpf = GpFunctions()
    print(gpf.get_fit_6())
