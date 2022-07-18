import os
import shutil

from condorgp.params import lean_dict, test_dict #


def run_lean():
    ''' simple but current Condorgp primary way to run lean fitness function.

    Requires:
        1 - Algorithm to be set (manual .py name here for now)
        2 - Configuration json to be set (also manual for now)

    Both 1 & 2 are copied into place in the Lean package.
    Then the run command is made
    '''
    # copy algo py into place
    copy_ind_to_lean_algos_dir(
        test_dict['CONDOR_CONFIG_PATH'],
        'IndBasicAlgo1.py')

    # copy .json across:
    copy_config_json_to_lean_launcher_dir(
        test_dict['CONDOR_CONFIG_PATH'],
        test_dict['CONDOR_TEST_CONFIG_FILE'])

    JSON_PATH = ''
    ALGO_PATH = lean_dict['LEAN_ALGOS_FOLDER']

    os. chdir("../Lean")
    os.system("pwd")
    os.system(f"lean backtest {ALGO_PATH}IndBasicAlgo1.py --lean-config {JSON_PATH}config_test_condor.json --verbose --output Backtests")
    os. chdir("../condorgp")


def copy_ind_to_lean_algos_dir(file_path, filename):
    src = file_path + filename
    dst = lean_dict['LEAN_ALGOS_FOLDER'] + filename
    shutil.copy(src, dst, follow_symlinks=True)

def copy_config_json_to_lean_launcher_dir(file_path, filename):
    src = file_path + filename
    print(src)
    # dst = lean_dict['LEAN_CONFIG_DIR'] + filename
    dst = '../Lean/' + filename
    print(dst)
    shutil.copy(src, dst, follow_symlinks=True)

if __name__ == "__main__":
    run_lean()
