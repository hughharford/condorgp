import os
import sys
from os import listdir
import glob

from os.path import isfile, join
import shutil
from datetime import datetime
import logging

# from file_read_backwards import FileReadBackwards

from condorgp.params import Params

import sys

class Utils:
    '''
        Various utility functions, hold all place for now
    '''

    def __init__(self):
        self.p = Params()
        self.NAUT_DICT = self.p.naut_dict
        NAUT_DICT = self.p.naut_dict
        TEST_DICT = self.p.test_dict
        UTIL_DICT = self.p.util_dict


    # FOR DELETION
    # def cp_ind_to_lean_algos(self, file_path, filename):
    #     '''
    #     Copy a file to the
    #         lean_dict['LOCALPACKAGES_PATH']
    #     '''
    #     if filename[-3:] != '.py':
    #         filename = filename + '.py'
    #     src = file_path + filename
    #     dst = self.p.lean_dict['LOCALPACKAGES_PATH'] + filename
    #     shutil.copy(src, dst, follow_symlinks=True)

    # def cp_config_to_lean_launcher(self, file_path, filename):
    #     '''
    #     Copy the file to
    #         lean_dict['LOCALPACKAGES_PATH']
    #     '''
    #     src_ingoing_config = file_path + filename
    #     dst_to_copy_to = self.p.lean_dict['LOCALPACKAGES_PATH'] + filename
    #     shutil.copy(src_ingoing_config, dst_to_copy_to, follow_symlinks=True)

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

    def confirm_file_extant(self, file_path):
        return os.path.isfile(file_path)

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
        with open(log_file_n_path) as frb:
            for l in (frb.readlines() [-lines:]):
                # print(l, end ='')
                count += 1
                if count > lines: break
                list_lines.append(str(l))
        return list_lines

    # def actually_get_last_x_lines() taking out FileReadBackwards
    def last_n_lines(self, fname, N):
        # opening file using with() method
        # so that file get closed
        # after completing work
        with open(fname) as file:
            # loop to read iterate
            # last n lines and print it
            for line in (file.readlines() [-N:]):
                print(line, end ='')

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
            max_lines_diff = 500):
        '''
            This requires finding two bits "near" each other in the log

            e.g.
            log line | text found
            _____________________
            6890: 'BACKTEST POST-RUN'
            6956: 'Sharpe Ratio (252 days):        15.966514528587545'
            6987: 'BACKTESTER-001-naut-run-06","message":"DISPOSED'

        '''

        # use these defaults if not provided. See params.py
        if log_file_n_path == "":
            log_file_n_path = self.NAUT_DICT['NAUTILUS_LOG_FILE']
        if lines == 0:
            lines = self.p.util_dict['NO_LOG_LINES']
        if backtest_id == "":
            backtest_id = self.NAUT_DICT['BACKTEST_ID_CURRENT']

        log_as_list = self.get_last_x_log_lines(lines, log_file_n_path)

        line_count = line_search_start = line_search_end = 0
        now_searching_for_key = 0
        if log_as_list is None:
            print("didn't find log list")
            return "nope", -1

        # careful here: searching from far end of logs, end/start are switched
        log_key_END_nb_start_point = '"BacktestEngine","message":" General Statistics"'
        x = "BACKTEST POST-RUN"
        log_key_START_nb_end_point = f'{backtest_id}","message":"STOPPED'

        v = 1 # view_fitness_search_criteria
        if v:
            print(f'log_key_START_nb_end_point: {log_key_START_nb_end_point}')
            print(f'log_key_END_nb_start_point: {log_key_END_nb_start_point}')

        # go through reversed list (it was read from the back of the log)
        initial_cut_list = []
        for i, line in enumerate(log_as_list):
            # print(line)
            if str(log_key_START_nb_end_point) in line: # START at end - nb reversed
                now_searching_for_key = 1 # now know where to start
                line_search_start = i
            if now_searching_for_key == 1:
                # print(line)
                initial_cut_list.append(line)
                if str(log_key_END_nb_start_point) in line: # END at start - nb reversed
                    line_search_end = i
                    now_searching_for_key = 2
                    if v ==1: print(now_searching_for_key)

        # print('initial cut list: \n')
        # print(initial_cut_list)
        if v ==1: print(f'line_search_start = {line_search_start}')
        if v ==1: print(f'line_search_end = {line_search_end}')

        if now_searching_for_key == 2:
            for i, line in enumerate(log_as_list): ## for simplicity
                if i > line_search_start and i < line_search_end:
                    # print(line)
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

    def count_lines_in_file(self, file_path):
        ''' returns no. of lines '''
        with open(file_path, 'r') as fp:
            lines = sum(1 for line in fp)
            print('Total Number of lines:', lines)
            return lines

    def keep_x_lines_of_log(self, log_file_path, no_last_lines=5000):
        ''' saves last x lines and calls method to writes down backups'''
        last_lines = self.get_last_x_log_lines(no_last_lines, log_file_path)
        os.remove(log_file_path)
        with open(log_file_path, "w") as renewed_log:
            for line in last_lines:
                renewed_log.write(line)
        renewed_log.close()

    def make_no_log_backups(self, log_file_path, no_backups=""):
        ''' saves backups up to specified number '''
        source = log_file_path
        if no_backups:
            backups = no_backups
        else:
            backups = self.NAUT_DICT['NUM_LOG_BACKUPS']
        if log_file_path:
            log = log_file_path
        else:
            log = self.NAUT_DICT['NAUTILUS_LOG_FILE']
        s = log.split(".")
        last_backup = s[0]+f'_old_{backups}.{s[1]}'
        if os.path.isfile(last_backup): os.remove(last_backup)
        for n in range(backups, 0, -1):
            dest_a = s[0]+f'_old_{n}.{s[1]}'
            dest_b = s[0]+f'_old_{n+1}.{s[1]}'
            if os.path.isfile(dest_a) and n < backups:
                shutil.copyfile(dest_a, dest_b)
                os.remove(dest_a)
        # copy most recent to
        dest = s[0]+f'_old_1.{s[1]}'
        shutil.copyfile(source, dest)

    # this is misplaced
    # def check_seq_only_ever_increases(self, seq):
    #     print("Original list : " + str(seq))
    #     # using zip() + all() to check for strictly increasing list
    #     r = all(i < j for i, j in zip(seq, seq[1:]))
    #     print("Is list strictly increasing ? : " + str(r))
    #     return r

    def check_seq_never_decreases(self, seq):
        print("Original list : " + str(seq))
        # using zip() + all() to check for strictly increasing list
        r = all(i <= j for i, j in zip(seq, seq[1:]))
        print("Is list never decreasing ? : " + str(r))
        return r

    def fix_number_for_sort(self, string_num):
        if string_num > 0 and string_num < 10:
            return f"000{string_num}"
        elif string_num > 10 and string_num < 100:
            return f"00{string_num}"
        elif string_num > 100 and string_num < 1000:
            return f"0{string_num}"

    def tidy_cp_files(self, cp_base):
        chpt_path = self.p.naut_dict['CHECKPOINT_PATH']
        # All files and directories ending with .txt and that don't begin with a dot:
        to_delete = glob.glob(f"{chpt_path}{cp_base}_*.pkl")
        to_delete.sort()
        for f in range(len(to_delete)-2):
            if to_delete[f] != chpt_path+cp_base+'_done.pkl':
                pass
                os.remove(to_delete[f])

    def check_paths_and_logs_extant(self):
        print("checking env and key folders established:")
        pathsetc = self.p.get_params("naut_dict")

        # 3 paths must exist
        LOGSFOLDER = os.path.isdir(pathsetc["LOGS_FOLDER"])
        CPFOLDER = os.path.isdir(pathsetc["CHECKPOINT_PATH"])
        NAUTILUSBASEFOLDER = os.path.isdir(pathsetc["NAUTILUS_BASE_PATH"])
        #2 log files must be extant:
        NAUTLOG = os.path.isfile(pathsetc["NAUTILUS_LOG_FILE"])
        CONDORLOG = os.path.isfile(pathsetc["CONDOR_LOG_FILE"])
        if LOGSFOLDER:
            print(f"Logs path present: {pathsetc["LOGS_FOLDER"]}")
        if CPFOLDER:
            print(f"Checkpoint path present: {pathsetc["CHECKPOINT_PATH"]}")
        if NAUTILUSBASEFOLDER:
            print(f"Nautilus log present, assumes installed: {pathsetc["NAUTILUS_BASE_PATH"]}")
        if CONDORLOG:
            print(f"Condor log present: {pathsetc["CONDOR_LOG_FILE"]}")

        if all([CONDORLOG, CONDORLOG, NAUTILUSBASEFOLDER, CPFOLDER, LOGSFOLDER]):
            return True
        else:
            return False

    def reset_logfile(self):
        log_file_n_path = p.naut_dict['NAUTILUS_LOG_FILE']
        print("resetting log")
        with open(log_file_n_path, 'w'):
            pass


if __name__ == "__main__":
    pass
    print('Utils run going...')



    u = Utils()
    # base = "new"
    # # u.tidy_cp_files(base) # tidying cp files
    # seq1 = [1,1,1,1,1,1,1,1,1,1,1] # 2,3,3,4,5,6]
    # seq2 = []
    # u.check_seq_never_decreases(seq1)
    p = Params()
    # key_req = p.naut_dict['SPECIFIED_FITNESS'] # p.naut_dict['FITNESS_CRITERIA']
    # log_file_n_path = p.naut_dict['NAUTILUS_LOG_FILE']
    # # print(f'{key_req}, {log_file_n_path}')
    # fitness = u.find_fitness_with_matching_backtest(
    #         key = key_req,
    #         log_file_n_path = "",
    #         backtest_id = "",
    #         lines = 0,
    #         max_lines_diff = 200)
    # print(fitness)

    # print(u.check_paths_and_logs_extant())

    f = 0.0

    # SUGGESTED NEW APPROACH FOR FITNESS FINDING




    # key_req = self.naut_dict['FITNESS_CRITERIA_AVG_RETURN']
    # key_req = p.naut_dict['FITNESS_CRITERIA_RISK_RETURN_RATIO']
    key_req = p.naut_dict['FITNESS_CRITERIA_SORTINO_RATIO']
    # key_req = self.naut_dict['FITNESS_CRITERIA_PNL_TOTAL']
    # key_req = self.naut_dict['FITNESS_CRITERIA_SHARPE_RATIO']
    # key_req = p.naut_dict['SPECIFIED_FITNESS']

    log_file_n_path = p.naut_dict['NAUTILUS_LOG_FILE']


    # @@@@@@@@@@@@@@@@@@@@@@@@@
    reset_logs = 1
    if reset_logs:
        u.reset_logfile()

    # @@@@@@@@@@@@@@@@@@@@@@@@@

    backtest_id="naut-run-04"

    filelength = u.count_lines_in_file(log_file_n_path)

    lines_to_check = 7000 # CAREFUL: TOO MANY LINES AND FAILS, default = 400
    max_lines_diff = 500 # default 500

    get_last_lines = 0
    if get_last_lines:
#        u.get_last_x_log_lines(10)

        fname = log_file_n_path
        print(log_file_n_path)
        N = 3
        try:
            u.last_n_lines(fname, N)
        except:
            print('File not found')


    find_fitness = 0
    if find_fitness:
        print("finding fitness with: >>>>> find_fitness_with_matching_backtest")
        try:
            got = u.find_fitness_with_matching_backtest(
                    key = key_req
                    , log_file_n_path = log_file_n_path # default: Nautilus log
                    , backtest_id = backtest_id
                    , lines = lines_to_check
                    , max_lines_diff = max_lines_diff
                    )
            foundfit = "" # if poor, set v low as < bad algorithms getting <0
            if got[1] != -1:
                foundfit = u.get_last_chars(got[0],3)
                f = -22000 # nan
            else:
                f = -111000 # not found
            if len(foundfit) > 3:
                f = float(u.get_last_chars(got[0],3))
            print(f)
        except BaseException as e:
            logging.error(f"ERROR {__name__}: {e}")
