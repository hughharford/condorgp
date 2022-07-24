import os
import shutil
from datetime import datetime

from file_read_backwards import FileReadBackwards

from condorgp.params import lean_dict, test_dict, util_dict


def copy_ind_to_lean_algos_dir(file_path, filename):
    '''
    Copy a file to the
        lean_dict['LEAN_ALGOS_FOLDER']
    '''
    src = file_path + filename
    dst = lean_dict['LEAN_ALGOS_FOLDER'] + filename
    shutil.copy(src, dst, follow_symlinks=True)

def copy_config_json_to_lean_launcher_dir(file_path, filename):
    '''
    Copy the file to
        lean_dict['LEAN_CONFIG_DIR']
    '''
    src = file_path + filename
    dst = lean_dict['LEAN_CONFIG_DIR'] + filename
    shutil.copy(src, dst, follow_symlinks=True)

def delete_file_from_path(file_path, filename):
    '''
    delete file func
    '''
    file_to_delete = file_path + filename
    ## If file exists, delete it ##
    if os.path.isfile(file_to_delete):
        os.remove(file_to_delete)
    else:    ## Show an error ##
        print("Error: %s file not found" % file_to_delete)

def check_recent_mod(input_file_paths):
    '''
    Returns true if all files in the path updated within
    'reasonable fitness seconds' set in params.py
    '''
    dt = datetime.now()
    now = datetime.timestamp(dt)
    diff = 1000*test_dict['REASONABLE_FITNESS_SECS']
    count = 0
    for file_path in input_file_paths:
        count += 1
        print(f'{file_path} and {now - diff}')
        if (now - diff) > os.path.getmtime(file_path): return False
        if count == 0: return False
    return True

def get_last_x_log_lines(
        lines = 150,
        log_file_n_path = lean_dict['BACKTEST_LOG']):
    '''
    Get from the (default) log the last X lines
    '''
    list_lines = []
    count = 0
    with FileReadBackwards(log_file_n_path, encoding="utf-8") as frb:
        for l in frb:
            count += 1
            if count > lines: break
            # print(l)
            list_lines.append(l)
    return list_lines

def retrieve_log_line_with_key(
        key,
        lines = 150,
        log_file_n_path = lean_dict['BACKTEST_LOG']):
    '''
    Get the X lines of a log
    And search for the key given

    Returns a tuple:
        the FIRST line if found, or '' if not found
        the count of line number, given the no. lines

        N.B. First from the last X lines of the log...
            But taken in reverse order, last first as end of the log file
    '''
    log_to_search_list = get_last_x_log_lines(lines, log_file_n_path)
    # return both the line and it's index, to indicate where it was found
    for i, line in enumerate(log_to_search_list):
        if str(key) in line: return line, i
    return '', -1

def get_keyed_line_within_limits(
        key,
        log_file_n_path = lean_dict['BACKTEST_LOG'],
        limit_lines = util_dict['NO_LOG_LINES'],
        start_line = 0)-> tuple:
    '''
    TO DO: Return a tuple of:
        The retrived line in full that contains X
        Provided within the limit_lines after Z found
        How many lines after the start_line is found
    '''
    found_tuple = retrieve_log_line_with_key(
        key = key,
        log_file_n_path = log_file_n_path)

    line = found_tuple[0]
    no_lines_after_start = found_tuple[1]

    if line == '' and no_lines_after_start == -1:
        return 'not found', -1
    elif no_lines_after_start < start_line:
        return f'below limit given: {limit_lines}', -2
    elif no_lines_after_start > limit_lines:
        return f'past limit given: {limit_lines}', -3
    return line, no_lines_after_start

def get_last_chars(line):
    temp = str.split(line,' ')
    return temp[-1]

def get_fitness_from_log(
        key = lean_dict['FITNESS_CRITERIA'],
        log_file_n_path = lean_dict['BACKTEST_LOG']):
    pass


if __name__ == "__main__":
    key1 = 'TRACE:: Engine.Run(): Disposing of setup handler...'
    key2 = 'STATISTICS:: Return Over Maximum Drawdown'
    key1_line_check = 6
    key2_line_check = 24
    got = get_keyed_line_within_limits(key2)
    print(got)

    assert got[0] != ''
    assert got[1] == key2_line_check

    print(get_last_chars(got[0]))
