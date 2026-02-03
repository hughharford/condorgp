#!usr/bin/env bash

str=$LOCAL_BASE_PATH
nn=`echo $str | awk '{print length}'`
echo "Start: Length of the LOCAL_BASE_PATH env variable is : $nn "

safety=1

if [ $nn -eq 0 ]; then
  echo "no LOCAL_BASE_PATH set"
else
  cd $LOCAL_BASE_PATH
  echo "then here $LOCAL_BASE_PATH"
  path="${LOCAL_BASE_PATH}tests/test_data/test_dir/"
  echo $path
  for dir in `ls -l $path | grep ^d | awk '{print $9}'`; do
    [ "$dir" = ".venv" ] && continue
    echo "going to delete $path$dir "
    rm -rf $path$dir
  done

  if [ $safety -eq 0 ]; then
    echo "safety read as $safety"
    cd ..
    mkdir cgp_temp
    mv condorgp/* cgp_temp
    rm condorgp
    git clone git@github.com:hughharford/condorgp.git
    cp -n cgp_temp/* condorgp/*
  fi
fi
