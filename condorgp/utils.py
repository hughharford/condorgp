import os
import shutil
from datetime import datetime


from condorgp.params import lean_dict, test_dict
from file_read_backwards import FileReadBackwards


def copy_ind_to_lean_algos_dir(file_path, filename):
    src = file_path + filename
    dst = lean_dict['LEAN_ALGOS_FOLDER'] + filename
    shutil.copy(src, dst, follow_symlinks=True)

def copy_config_json_to_lean_launcher_dir(file_path, filename):
    src = file_path + filename
    # print(src)
    # dst = lean_dict['LEAN_CONFIG_DIR'] + filename
    dst = '../Lean/' + filename
    # print(dst)
    shutil.copy(src, dst, follow_symlinks=True)

def delete_file_from_path(file_path, filename):
    file_to_delete = file_path + filename
    ## If file exists, delete it ##
    if os.path.isfile(file_to_delete):
        os.remove(file_to_delete)
    else:    ## Show an error ##
        print("Error: %s file not found" % file_to_delete)

def get_last_x_log_lines(lines = 150, log_file_n_path = '/home/hsth/code/hughharford/Lean/Backtests/log.txt'):
    list_lines = []
    count = 0
    with FileReadBackwards(log_file_n_path, encoding="utf-8") as frb:
        for l in frb:
            count += 1
            if count > lines: break
            print(l)
            list_lines.append(l)
    return list_lines

def retrieve_log_line_with_key(
                    key,
                    lines = 150,
                    log_file_n_path = '/home/hsth/code/hughharford/Lean/Backtests/log.txt'):
    '''
    Get the X lines of a log
    And search for the key given

    Returns the FIRST line if found, or '' if not found
    '''
    log_to_search_list = get_last_x_log_lines(lines, log_file_n_path)
    for line in log_to_search_list:
        if str(key) in line: return line
    return ''

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

if __name__ == "__main__":
    results_files = [lean_dict['LEAN_RESULTS_FOLDER'] + x for
                     x in os.listdir(lean_dict['LEAN_RESULTS_FOLDER'])
                     if os.path.isfile(lean_dict['LEAN_RESULTS_FOLDER'] + x)]
    assert check_recent_mod(results_files)
