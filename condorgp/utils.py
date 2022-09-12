import os
import shutil
from datetime import datetime

from file_read_backwards import FileReadBackwards

from condorgp.params import lean_dict, test_dict, util_dict


def cp_ind_to_lean_algos(file_path, filename):
    '''
    Copy a file to the
        lean_dict['LEAN_ALGOS_FOLDER']
    '''
    if filename[-3:] != '.py':
        filename = filename + '.py'
    src = file_path + filename
    dst = lean_dict['LOCALPACKAGES_PATH'] + filename
    shutil.copy(src, dst, follow_symlinks=True)


def cp_config_to_lean_launcher(file_path, filename):
    '''
    Copy the file to
        lean_dict['LEAN_CONFIG_DIR']
    '''
    src_ingoing_config = file_path + filename
    dst_to_copy_to = lean_dict['LOCALPACKAGES_PATH'] + filename
    shutil.copy(src_ingoing_config, dst_to_copy_to, follow_symlinks=True)

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

def get_all_lines(file_input):
    lines = open(file_input).readlines()
    return lines

def get_last_x_log_lines(
        lines = 150,
        log_file_n_path = lean_dict['BACKTEST_LOG_LOCALPACKAGES']):
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
        log_file_n_path = lean_dict['BACKTEST_LOG_LOCALPACKAGES']):
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
        log_file_n_path = lean_dict['BACKTEST_LOG_LOCALPACKAGES'],
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
        log_file_n_path = lean_dict['BACKTEST_LOG_LOCALPACKAGES']):
    pass

def overwrite_main_with_input_ind(input_ind):
    '''
    Replace main.py with our algorithm, from an existing .py file
    '''
    cp_rename_algo_to_main(input_ind)
    rename_main_class_as_condorgp()

def cp_rename_algo_to_main(input_ind):
    '''
    Rename file to main.py

    Requires our algo to be in the localpackages path
    '''
    f_path = lean_dict['LOCALPACKAGES_PATH']
    if input_ind[-3:] != '.py':
        input_ind = input_ind + '.py'
    src = f_path + input_ind
    dst = f_path + 'main.py'
    if src and dst:
        shutil.copy(src, dst, follow_symlinks=True)

def rename_main_class_as_condorgp():
    '''
    Rename the class in the main.py to:
        class condorgp(QCAlgorithm)
    '''
    f_path = lean_dict['LOCALPACKAGES_PATH']
    key_line = 'class'
    replacement_line = "class condorgp(QCAlgorithm): \n"
    main_py_for_class_rename = f_path + 'main.py'

    with open(main_py_for_class_rename, 'r') as f:
        lines = f.readlines()

    with open(main_py_for_class_rename, 'w') as f:
        count = 0
        for line in lines:
            if key_line in line and count == 0:
                line = replacement_line
                count += 1
            f.write(line)

if __name__ == "__main__":
    pass
    print('going...')
    input_ind = 'IndBasicAlgo1.py'
    overwrite_main_with_input_ind(input_ind)
