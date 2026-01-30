#!/bin/bash

# poetry install \
#                     --no-root \
#                     --without api \
#                     --without database \
#                     --without cluster \
#                     --without cloud \
#                     --without test \
#                     --without dev \
#                     --without optional

# poetry run
python condorgp/cgp_rabbitmq/delegate/run_delegated_evals_4_w_strat.py
