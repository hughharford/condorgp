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

pip3 install pika file_read_backwards;
python cgp_rabbitmq/delegate/run_delegated_evals_3_run_naut.py
