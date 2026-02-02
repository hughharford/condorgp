#!/bin/bash

echo "Checking required utility folders, logs and checkpoints."
echo "Current path:"
pwd
echo " "

DIR1="condorgp/util/logs"
if [ -d "$DIR1" ]; then
    echo "logs Directory exists."
else
    echo "logs Directory does not exist, creating now with files."
    mkdir condorgp/util/logs
    touch condorgp/util/logs/condor_log.txt
    touch condorgp/util/logs/nautilus_log.json
fi

DIR2="condorgp/util/checkpoints"
if [ -d "$DIR2" ]; then
    echo "checkpoints Directory exists."
else
    echo "checkpoints Directory does not exist, creating folder now."
    mkdir condorgp/util/checkpoints
fi

sudo chmod 777 -R condorgp/util/logs
sudo chmod 777 -R condorgp/util/checkpoints
