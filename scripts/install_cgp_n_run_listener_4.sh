#!/bin/bash
# # works, so avoiding:
#       pip3 install --ignore-installed poetry==1.8.4
#       pip install pika
#       pip3 install pika file_read_backwards;
#       poetry install --only-root; # minimal didn't work, but just needed poetry run python script.py (!)
#       poetry install; # full install somehow required, worth it for now


# poetry install
#     # full install works, but kinda heavy



pwd;

# trying this, to avoid all sorts of long installs on the worker start
poetry install --without api \
               --without database \
               --without cluster \
               --without cloud \
               --without test \
               --without dev \
               --without optional

#                   # --without primary \
#                   # --without evolution \
#                   # --without comms \

poetry run python cgp_rabbitmq/delegate/run_delegated_evals_4_w_strat.py

# # for use to keep the container runnning in case of debug need
# while :
# do
# 	echo "Press [CTRL+C] to stop.."
# 	sleep 1
# done
