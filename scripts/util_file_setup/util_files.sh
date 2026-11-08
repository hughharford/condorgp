#!/bin/bash

if condorgp/util/logs
  echo "logs exist"
then
  mkdir condorgp/util/logs
  touch condorgp/util/logs/condor_log.txt

fi

try
  mkdir condorgp/util/checkpoints
  touch condorgp/util/checkpoints/example.pkl
