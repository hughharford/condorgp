import os
import shutil

from condorgp.params import lean_dict, test_dict #
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

def alternative_from_file_end():
    with open('logfile.txt', 'rb') as f:
        f.seek(-2, os.SEEK_END)
    while f.read(1) != b'\n':
        f.seek(-2, os.SEEK_CUR)
    print(f.readline().decode())

if __name__ == "__main__":
    get_last_x_log_lines()
