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
# poetry install
# should be able to avoid this install....

# poetry run python cgp_db/main_api.py

# NEEDS A SERVICE

# # # for use to keep the container runnning in case of debug need
while :
do
	echo "Press [CTRL+C] to stop.."
	sleep 1
done

# WORKS ON STAR
