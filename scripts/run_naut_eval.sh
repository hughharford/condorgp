#!/bin/bash

poetry install \
                    --no-root \
                    --without api \
                    --without database \
                    --without cluster \
                    --without cloud \
                    --without test \
                    --without dev \
                    --without optional

# sleep 5m

# poetry run python condorgp/cgp_rabbitmq/delegate/delegate_eval.py
python condorgp/cgp_rabbitmq/delegate/delegate_eval.py

# sleep 5m
