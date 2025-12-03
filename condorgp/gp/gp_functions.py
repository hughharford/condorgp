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

    def get_fit_nautilus_1(self):
        f = 0.0
        lines_to_check = 10000
        log_file = self.naut_dict['NAUTILUS_LOG_FILE'] # check Nautilus log!

        latest_log = self.util.get_last_x_log_lines(lines = lines_to_check,
                                                    log_file_n_path = log_file)
        if latest_log:
            # if no errors, retrieve fitness
            fitness_line = self.naut_dict['FITNESS_CRITERIA'] # Sharpe's Ratio
            # try this instead:
            fitness_line = self.naut_dict['SIMPLE_FITNESS_CRITERIA'] # Risk Return Ratio
            lim = lines_to_check - 1
            got = self.util.get_key_line_in_lim(key = fitness_line,
                                                log_filepath = log_file,
                                                lines = lim)
            # print(got[0])
            foundfit = self.util.get_last_chars(got[0], ignore_last_chars = 2)
            if len(foundfit) > 3:
                f = float(self.util.get_last_chars(got[0], ignore_last_chars = 2))
            else:
                f = -1.0
            logging.debug(f'<<< gpf.get_fit_nautilus_1 fitness = {f}, from {log_file}')
        else:
            f = -8888.8 # no backtest folder found
            logging.warning(f'<<< gpf.get_fit_nautilus_1 fitness {f}, no file/folder found @ {log_file}')
        if f > 50:
            f = -1111.1 # set low if unrealistic!
            logging.warning(f'<<< gpf.get_fit_nautilus_1 fitness = {f}, as > 50 and unrealistic')
        return f

    def find_fitness(self, backtest_id="", log_file_n_path=""):
        '''
            finds fitness number (based on criteria)
            from Nautilus logs, within a set no. of lines close to a "run id"
        '''
        f = 0.0

        # key_req = self.naut_dict['FITNESS_CRITERIA_AVG_RETURN']
        # key_req = self.naut_dict['FITNESS_CRITERIA_RISK_RETURN_RATIO']
        # key_req = self.naut_dict['FITNESS_CRITERIA_PNL_TOTAL']
        # key_req = self.naut_dict['FITNESS_CRITERIA_SHARPE_RATIO']
        key_req = self.naut_dict['SPECIFIED_FITNESS']

        if backtest_id == "":
            backtest_id = self.naut_dict['BACKTEST_ID_CURRENT'] # preferred
            # backtest_id = "naut-run-06" # Hard coded default if not specified
        lines_to_check = self.naut_dict['LOG_LINES_TO_CHECK']
        # CAREFUL: TOO MANY LINES AND FAILS, default = 400
        max_lines_diff = self.naut_dict['MAX_LINES_DIFF'] # default 500

        try:
            got = self.util.find_fitness_with_matching_backtest(
                    key = key_req
                    , log_file_n_path = log_file_n_path # default: Nautilus log
                    , backtest_id = backtest_id
                    , lines = lines_to_check
                    , max_lines_diff = max_lines_diff
                    )
            foundfit = "" # if poor, set v low as < bad algorithms getting <0
            if got[1] != -1:
                foundfit = self.util.get_last_chars(got[0],2)
                f = -22000 # nan
            else:
                f = -111000 # not found
            if len(foundfit) > 3:
                f = float(self.util.get_last_chars(got[0],2))
        except BaseException as e:
            logging.error(f"ERROR {__name__}: {e}")
        return f

if __name__ == "__main__":
    gpf = GpFunctions()
    print(gpf.find_fitness(backtest_id="naut-run-06"))
