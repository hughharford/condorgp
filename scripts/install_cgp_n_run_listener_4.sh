#!/bin/bash

# pip3 install --ignore-installed poetry==1.8.4
# poetry install

#     # full install works, but kinda heavy
# # pip install pika

# poetry install --without api \
#                --without database \
#                --without cluster \
#                --without cloud \
#                --without test \
#                --without dev \
#                --without optional

#                   # --without primary \
#                   # --without evolution \
#                   # --without comms \

pwd;
# poetry install --only-root;
poetry install; # full install somehow required, worth it for now
# pip3 install pika file_read_backwards;
poetry run python cgp_rabbitmq/delegate/run_delegated_evals_4_w_strat.py
# while :
# do
# 	echo "Press [CTRL+C] to stop.."
# 	sleep 1
# done
