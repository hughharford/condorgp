#!/bin/bash

# QUANTCONNECT.COM - Democratizing Finance, Empowering Individuals.
# Lean Algorithmic Trading Engine v2.0. Copyright 2014 QuantConnect Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

## HSTH notes:
#
# This is a rework of a 2020 Lean file, useful for docker run mount etc
#
# getting the results folder to be leanQC/results would be ideal.
# this .sh file needs to be run from ../../QuantConnect/Lean
#
# NOTES:
#
# 1. default image to be a local lean:latest
# 2. update to paths, to run from here ,assume Lean is statically
#        ../../QuantConnect/Lean

full_path=$(realpath $0)
current_dir=$(dirname $full_path)
actual_lean_dir=/home/hsth/code/hughharford/Lean
default_image=lean:latest
default_launcher_dir=$actual_lean_dir/Launcher/bin/Debug
raw_launcher_dir=$actual_lean_dir/Launcher
default_data_dir=$actual_lean_dir/Data
default_results_dir=$current_dir/results
# default_config_file=$default_launcher_dir/config.json
default_config_file=/Launcher/bin/Debug/config_test_condor.json


# if [ -f "$1" ]; then
#     IFS="="
#     while read -r key value; do
#         eval "$key='$value'"
#     done < $1
# else
#     read -p "Enter docker image [default: $default_image]: " image
#     read -p "Enter absolute path to Lean binaries [default: $default_launcher_dir]: " launcher_dir
#     read -p "Enter absolute path to Lean config file [default: $default_config_file]: " config_file
#     read -p "Enter absolute path to Data folder [default: $default_data_dir]: " data_dir
#     read -p "Enter absolute path to store results [default: $default_results_dir]: " results_dir
# fi

if [ -d "$image" ]; then
    echo "Lean docker image $default_image does not exist"
    exit 1
fi

if [ -z "$launcher_dir" ]; then
    launcher_dir=$default_launcher_dir
fi

if [ ! -d "$launcher_dir" ]; then
    echo "Lean binaries directory $launcher_dir does not exist"
    exit 1
fi

if [ -z "$config_file" ]; then
    config_file=$default_config_file
fi

# if [ ! -f "$config_file" ]; then
#     echo "Lean config file $config_file does not exist"
#     exit 1
# fi

if [ -z "$data_dir" ]; then
    data_dir=$default_data_dir
fi

if [ ! -d "$data_dir" ]; then
    echo "Data directory $data_dir does not exist"
    exit 1
fi

if [ -z "$results_dir" ]; then
    results_dir=$default_results_dir
fi

if [ ! -d "$results_dir" ]; then
    echo "Results directory $results_dir does not exist"
    exit 1
fi

# sudo
sudo docker run --rm --mount type=bind,source=$launcher_dir,target=/root/Lean \
 --mount type=bind,source=$data_dir,target=/Data \
 --mount type=bind,source=$results_dir,target=/Results \
 lean:latest --data-folder /Data --results-destination-folder /Results --config $config_file
