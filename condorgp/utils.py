import os
import shutil

from condorgp.params import lean_dict #


def run_lean_bash_script():
    # subprocess.run(["bash","leanQC/run_docker.sh"])
    os.system("sh leanQC/run_docker.sh")

def copy_ind_to_lean_algos_dir(ind_file_and_path):
    src = ind_file_and_path
    dst = lean_dict['LEAN_ALGOS_FOLDER']
    shutil.copy(src, dst, follow_symlinks=True)

def copy_config_json_to_lean_launcher_dir(ind_file_and_path):
    src = ind_file_and_path
    dst = lean_dict['LEAN_CONFIG_FOLDER']
    shutil.copy(src, dst, follow_symlinks=True)
