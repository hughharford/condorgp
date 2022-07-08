from condorgp.params import lean_dict, test_dict
import os

def runner_working():
    results_path = lean_dict['LEAN_RESULTS_FOLDER']
    individual = results_path + 'BasicTemplateFrameworkAlgorithm'
    # leanQC/results/BasicTemplateFrameworkAlgorithm
    results_files = [results_path + x for x in os.listdir(results_path)]
    found_algo_name = False
    for folder_or_file in results_files:
        print(folder_or_file)
        if folder_or_file == individual:
            found_algo_name = True
    assert found_algo_name
    print(found_algo_name)

if __name__ == "__main__":
    runner_working()
