import os
import sys
from os import listdir
from os.path import isfile, join
import shutil
from datetime import datetime
import logging

from file_read_backwards import FileReadBackwards

from condorgp.params import Params
from condorgp.gp.gp_custom_functions import GpCustomFunctions

import sys

class Utils:
    '''
        Various utility functions, hold all place for now
    '''

    def __init__(self):
        self.cfs = GpCustomFunctions()
        self.p = Params()
        self.NAUT_DICT = self.p.naut_dict
        NAUT_DICT = self.p.naut_dict
        TEST_DICT = self.p.test_dict
        UTIL_DICT = self.p.util_dict


    def cp_ind_to_lean_algos(self, file_path, filename):
        '''
        Copy a file to the
            lean_dict['LOCALPACKAGES_PATH']
        '''
        if filename[-3:] != '.py':
            filename = filename + '.py'
        src = file_path + filename
        dst = self.p.lean_dict['LOCALPACKAGES_PATH'] + filename
        shutil.copy(src, dst, follow_symlinks=True)

    def cp_config_to_lean_launcher(self, file_path, filename):
        '''
        Copy the file to
            lean_dict['LOCALPACKAGES_PATH']
        '''
        src_ingoing_config = file_path + filename
        dst_to_copy_to = self.p.lean_dict['LOCALPACKAGES_PATH'] + filename
        shutil.copy(src_ingoing_config, dst_to_copy_to, follow_symlinks=True)

    def delete_file_from_path(self, file_path, filename):
        '''
        delete file func
        '''
        file_to_delete = file_path + filename
        ## If file exists, delete it ##
        if os.path.isfile(file_to_delete):
            os.remove(file_to_delete)
        else:    ## Show an error ##
            print("Error: %s file not found" % file_to_delete)

    def check_recent_mod(self, input_file_paths):
        '''
        Returns true if all files in the path updated within
        'reasonable fitness seconds' set in params.py
        '''
        dt = datetime.now()
        now = datetime.timestamp(dt)
        diff = 1000*self.p.test_dict['REASONABLE_FITNESS_SECS']
        count = 0
        recent = 0
        onlyfiles = [f for f in listdir(input_file_paths) if isfile(join(input_file_paths, f))]
        for file_path in onlyfiles:
            count += 1
            if (now - os.path.getmtime(input_file_paths +'/'+ file_path)) < (now - diff): recent += 1
        if count == 0: return False
        if recent > 0: return True

    def get_latest_log_dir(self):
        return self.NAUT_DICT['LOGS_FOLDER']

    def get_log_filepath(self, specific_log = 'condor_log'):
        if specific_log == 'condor_log':
            return self.NAUT_DICT['CONDOR_LOG_FILE']
        elif specific_log == 'nautilus_log':
            return self.NAUT_DICT['NAUTILUS_LOG_FILE']
        else:
            return "Specify log: use either 'condor_log' or 'nautilus_log'"



    def get_latest_log_content(self, specific_log = 'condor_log'):
        if specific_log == 'condor_log':
            log_file = self.NAUT_DICT['CONDOR_LOG_FILE']
        elif specific_log == 'nautilus_log':
            log_file = self.NAUT_DICT['NAUTILUS_LOG_FILE']
        else:
            return "No specific log provided: use either 'condor_log' or 'nautilus_log'"
        return self.get_all_lines(log_file)

    def get_all_lines(self, file_input):
        try:
            lines = open(file_input).readlines()
        except:
            print(f'ERROR opening this file: {file_input}')
            return []
        return lines

    def get_last_x_log_lines(self, lines = 400, log_file_n_path = ""):
        '''
        Get from the (default) log the last X lines
        '''
        if log_file_n_path == "":
            log_file_n_path = self.NAUT_DICT['NAUTILUS_LOG_FILE']

        list_lines = []
        count = 0
        with FileReadBackwards(log_file_n_path, encoding="utf-8") as frb:
            for l in frb:
                count += 1
                if count > lines: break
                # print(l)
                list_lines.append(str(l))
        return list_lines

    def confirm_ind_name_in_log_lines(self,output_ind, log_file_n_path = ""):
        '''
        To identify if the named evolved individual is found in
        the specified log within the specified lines
        '''
        if log_file_n_path == "":
            log_file_n_path = self.p.naut_dict['NAUTILUS_LOG_FILE']

        # print(output_ind)
        results_list = self.get_last_x_log_lines(
                    log_file_n_path,
                    lines =  self.p.util_dict['NO_LOG_LINES']
                    )
        found_algo_name = False
        for line in results_list:
            if output_ind in line:
                # print(line)
                found_algo_name = True
        return found_algo_name

    def retrieve_log_line_with_key(self,
            key,
            lines = 0,
            log_file_n_path = ""):
        '''
        Get the X lines of a log
        And search for the key given

        Returns a tuple:
            the FIRST line if found, or '' if not found
            the count of line number, given the no. lines

            N.B. First from the last X lines of the log...
                But taken in reverse order, last first as end of the log file
        '''
        if log_file_n_path == "":
            log_file_n_path = self.NAUT_DICT['NAUTILUS_LOG_FILE']
        if lines == 0:
            lines = self.p.util_dict['NO_LOG_LINES']

        log_to_search_list = self.get_last_x_log_lines(lines, log_file_n_path)
        # return both the line and it's index, to indicate where it was found
        for i, line in enumerate(log_to_search_list):
            # print(line)
            if str(key) in line: return line, i
        return '', -1

    def get_key_line_in_lim(self,
            key,
            log_filepath = "",
            lines = 0,
            start_line = 0)-> tuple:
        '''
        TO DO: Return a tuple of:
            The retrived line in full that contains X
            Provided within the limit_lines after Z found
            How many lines after the start_line is found
        '''
        if log_filepath == "":
            log_filepath = self.NAUT_DICT['NAUTILUS_LOG_FILE']
        if lines == 0:
            lines = self.p.util_dict['NO_LOG_LINES']

        found_tuple = self.retrieve_log_line_with_key(
            key = key,
            log_file_n_path = log_filepath,
            lines = lines)

        found_line = found_tuple[0]
        no_lines_after_start = found_tuple[1]

        if found_line == '' and no_lines_after_start == -1:
            return 'not found', -1
        elif no_lines_after_start < start_line:
            return f'below limit given: {lines}', -2
        elif no_lines_after_start > lines:
            return f'past limit given: {lines}', -3
        return found_line, no_lines_after_start

    def find_fitness_with_matching_backtest(self,
            key,
            log_file_n_path = "",
            backtest_id = "",
            lines = 0,
            max_lines_diff = 0):
        '''
            This requires finding two bits "near" each other in the log

            e.g.
            log line | text found
            _____________________
            54532: 'BACKTESTER-001-naut-runner-04","message":"STOPPED."'
            54554: '\u001b[36m BACKTEST POST-RUN'
            54620: 'Sharpe Ratio (252 days):        15.966514528587545'

        '''

        if log_file_n_path == "":
            log_file_n_path = self.NAUT_DICT['NAUTILUS_LOG_FILE']
        if lines == 0:
            lines = self.p.util_dict['NO_LOG_LINES']

        log_as_list = self.get_last_x_log_lines(lines, log_file_n_path)

        first_key_for_backtest = f'{backtest_id}","message":"STOPPED."'
        second_key_for_run_end = "BACKTEST POST-RUN"


        line_count = 0
        now_searching_for_key = 0
        if log_as_list is None:
            print("didn't find log list")
            return "nope", -1

        print(first_key_for_backtest)
        print(second_key_for_run_end)

        # go through reversed list (it was read from the back of the log)
        log_as_list.reverse()
        for i, line in enumerate(log_as_list):
            # print(line)
            if str(first_key_for_backtest) in line:
                now_searching_for_key = 1 # now know where to start
            if now_searching_for_key == 1:
                if str(second_key_for_run_end) in line:
                    now_searching_for_key = 2
                    # print(now_searching_for_key)
            if now_searching_for_key == 2:
                if str(key) in line: return line, i
                line_count += 1
            if line_count > max_lines_diff:
                 return "too many lines", -1
        return 'nothing found here', -1

    def get_last_chars(self, line, ignore_last_chars = 0):
        if ignore_last_chars:
            line = line[0:-ignore_last_chars] # remove last chars to ignore
        temp = str.split(line,' ')
        return temp[-1]

    def print_sys_path(self):

        a = '/home/hsth/.pyenv/versions/nautilus/bin'
        b = '/home/hsth/.pyenv/versions/3.10.8/bin/python3.10'

        naut_venv_s_packages = '/home/hsth/.pyenv/versions/nautilus/lib'
        # for nautilus, from other venv
        sys.path.append(naut_venv_s_packages)
        sys.path.append(a)
        sys.path.append(b)

        for p in sys.path:
            print(p)

    def write_to_file(self, filename_n_path, inputtext, mode = "a"):
        # utils method to enable writing to sourced file wherever, AWS, local...
        try:
            f = open(filename_n_path, mode)
            f.write(inputtext)
            f.close()
        except:
            logging.error(f"utils.write_to_file: \
                           filename n path: {filename_n_path}")
            return None

if __name__ == "__main__":
    pass
    print('going...')
    u = Utils()
    key_req = 'Sharpe Ratio (252 days)'
    # key3 = "Sharpe Ratio"
    # key2 = "EMACross-000"
    lines = 2000

    # no error here, just need to provide lines = X enough to find it...
    # found2 = u.retrieve_log_line_with_key(
    #     key = key_req,
    #     lines = lines)
    # print(f"found2 = {found2[0]}")

    # actually a key finding issue
    # found3 = u.get_key_line_in_lim(
    #     key = key_req,
    #     lines = lines)
    # # print(f"found3 = {found3}")

    # expected = -21.49663142709111

    # here = float(u.get_last_chars(found3[0],2))
    # assert here == expected

    expected = -21.49663142709111
    # for dev only:
    backtest_id = "naut-runner-03"
    key_fitness = Params().naut_dict['FITNESS_CRITERIA']
    print(key_fitness)
    found4 = u.find_fitness_with_matching_backtest(
            key = key_fitness,
            log_file_n_path = "",
            backtest_id = backtest_id,
            lines = 55000,
            max_lines_diff = 22000)
    print(found4[0])
    here = float(u.get_last_chars(found4[0],2))
    assert here == expected
