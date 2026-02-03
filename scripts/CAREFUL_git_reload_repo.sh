#!usr/bin/env bash

# SET UP PATHS
# RETREAT and READY
# SAVE FILES
# DELETE FOLDERS EXCEPT .venv
# GIT CLONE
# COPY FILES BACK IN

# SET UP PATHS
current_dir=$(pwd)
echo "The script is running from: $current_dir"
copy_from_path=$current_dir/condorgp/
echo "copy_from_path : $copy_from_path"
to_path=$current_dir/cgp_files_temp/
echo "to_path : $to_path"
copy_back_to_path=$current_dir/condorgp/
echo "copy_back_to_path : $copy_back_to_path"
copy_from_saved_path=$to_path
echo "copy_from_saved_path : $copy_from_saved_path"

# RETREAT and READY
ready=1
if [ $ready -eq 1 ]; then
  # cd .. ## assume already in parent folder, no need for ..
  temp_dir="cgp_files_temp"
  mkdir -p $temp_dir
fi

# SAVE FILES
copy_files=1
if [ $copy_files -eq 1 ]; then
  echo "copy_files read as $copy_files, current dir = $current_dir"
  echo "going to copy across to $to_path:"
  for f in $(ls -p -a "$copy_from_path" | grep -v /); do
    cp $copy_from_path$f $to_path
  done

else
  echo "would retreat and save files here"
fi

# DELETE FOLDERS EXCEPT .venv
delete_folders=0
if [ $delete_folders -eq 1 ]; then
  # echo "HERE HERE HERE $copy_from_path"
  # path="${copy_from_path}tests/test_data/test_dir/"
  echo "DELETE FROM: $copy_from_path"
  for dir in `ls -la $copy_from_path | grep ^d | awk '{print $9}'`; do
    [ "$dir" = ".venv" ] && echo "skipping .venv" && continue
    [ "$dir" = ".." ] && echo "skipping .." && continue
    [ "$dir" = "." ] && echo "skipping ." && continue
    echo "going to delete $copy_from_path$dir "
    rm -rf $path$dir
  done
else
  echo "would delete folders except .venv here"
fi

clone_repo=0
if [ $clone_repo -eq 1 ]; then
  echo "clone it now"
  # rm condorgp
  # git clone git@github.com:hughharford/condorgp.git
  # cp -n cgp_temp/* condorgp/*
else
  echo "would clone here"
fi

# COPY FILES BACK IN
copy_files_back=1
if [ $copy_files_back -eq 1 ]; then

  echo "copy_files read as $copy_files_back, copy from: $copy_from_saved_path to $copy_back_to_path "

  # echo "going to copy across to $copy_back_to_path:"
  for f in $(ls -p -a "$copy_from_saved_path" | grep -v /); do
    cp $copy_from_saved_path$f $copy_back_to_path
  done

else
  echo "would retreat and save files here"
fi
