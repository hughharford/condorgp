from condorgp.params import Params
import shutil

class GPReadyEvolvedCode():

    def __init__(self):
        self.p = Params()
        self.NAUT_DICT = self.p.naut_dict

    def cp_ind_to_lean_algos(self, file_path, filename):
        '''
        Copy a file to the
            lean_dict['LOCALPACKAGES_PATH']
        '''
        if filename[-3:] != '.py':
            filename = filename + '.py'
        src = file_path + filename
        dst = self.NAUT_DICT['NAUTILUS_EVAL_PATH'] + filename
        shutil.copy(src, dst, follow_symlinks=True)

    # FIRST PASS SORTED ABOVE THIS LINE:
    # =========================================================================

    def cp_inject_algo_in_n_sort(self, base_algo_name_ext, inj_str):
        '''
        Take evolved code, and inject. then copy across to
        localpackages, renamed file and class declaration.
        '''
        # # check and wrap evolved code if need be:
        # if 'def' not in inj_str:
        #     inj_str = self.wrap_injection_str(inj_str)

        # inject evolved code into algo py file
        self.inject_evolved_func_in(base_algo_name_ext, inj_str)
        # copy file across:
        done_injectedAlgo_to_copy_in = self.NAUT_DICT['CGP_NAUT_STRATEGIES']
        self.copy_algo_in(done_injectedAlgo_to_copy_in)
        # rename 'gpInjectAlgo_done.py' to main.py
        self.cp_rename_algo_file_to_main('gpInjectAlgo_done.py')
        # go into gpInjectAlgo_done.py and rename class to condorgp:
        self.rename_main_class_as_condorgp(gpInjectAlgo_class_line = True)

    # ?????????????????????
    # Is this needed in any way?
    def wrap_injection_str(self, inj_str):
        try:
            content = eval(f'self.cfs.{inj_str}')
            print(' >>>>>>>>>>>>>>>>>> UTILS.wrap_injection_str: ', content)
            return content
        except Exception as e:
            print(f'UTILS.wrap_injection_str FAILED: {inj_str}, {str(e)}')

    def inject_evolved_func_in(self,
                               base_algo_name_ext,
                               str_for_injection = ''):
        '''
        Inject the evolved function into the local:
            class gpInjectAlgo(QCAlgorithm)
        N.B.
        This then needs copying across into Local Packages, renaming etc
        '''
        config_path = lean_dict['CONDOR_CONFIG_PATH']
        f_name_n_path = config_path + lean_dict['LEAN_TO_INJECT_TEMPLATE_ALGO']
        f_name_n_path = f_name_n_path[0:-3] + base_algo_name_ext
        f_new_file = config_path + lean_dict['LEAN_INJECTED_ALGO']
        key_line = '## INJECT GP CODE HERE:'
        # careful here, the indentation is crucial,
        # see initial replacement line string:
        replacement_line = '''
    def newly_injected_code(self, data_in):
        self.Debug("eval_test_XX: injected_code_test {data_in}")'''
        if str_for_injection != '':
            replacement_line = str_for_injection
        with open(f_name_n_path, 'r') as f:
            lines = f.readlines()
        with open(f_new_file, 'w') as f:
            count = 0
            next = 0
            for line in lines:
                if key_line in line and count == 0: count += 1
                if next == 1: line = replacement_line
                if count > 0: next += 1
                f.write(line)

    def rename_main_class_as_condorgp(self, gpInjectAlgo_class_line = False):
        '''
        Rename the class in the main.py to:
            class condorgp(QCAlgorithm)
        NB. Requires:
            1. file to be main.py
            2. in the Lean localpackages folder
        '''
        f_path = lean_dict['LOCALPACKAGES_PATH']
        key_line = 'class'
        replacement_line = "class condorgp(QCAlgorithm): \n"
        if gpInjectAlgo_class_line:
            replacement_line = "class gpInjectAlgo(QCAlgorithm): \n"
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

    def copy_algo_in(self, input_ind):
        # copy algo.py across before container launch
        test_ind_path = lean_dict['CONDOR_CONFIG_PATH']
        self.cp_ind_to_lean_algos(test_ind_path, input_ind)
        self.overwrite_main_with_input_ind(input_ind)


    def overwrite_main_with_input_ind(self,input_ind):
        '''
        Replace main.py with our algorithm, from an existing .py file
        '''
        if input_ind[-3:] != '.py':
            input_ind = input_ind + '.py'
        self.cp_rename_algo_file_to_main(input_ind)
        self.rename_main_class_as_condorgp()

    def cp_rename_algo_file_to_main(self, input_ind):
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
