import os
import shutil

from condorgp.params import lean_dict #


def run_lean_bash_script():
    # subprocess.run(["bash","leanQC/run_docker.sh"])
    os.system("sh leanQC/run_docker.sh")

def copy_ind_to_lean_algos_dir(file_path, filename):
    src = file_path + filename
    dst = lean_dict['LEAN_ALGOS_FOLDER'] + filename
    shutil.copy(src, dst, follow_symlinks=True)

def copy_config_json_to_lean_launcher_dir(file_path, filename):
    src = file_path + filename
    dst = lean_dict['LEAN_CONFIG_DIR'] + filename
    shutil.copy(src, dst, follow_symlinks=True)

if __name__ == "__main__":
    run_lean_bash_script()
