#!/bin/bash

# # # for use to keep the container runnning in case of debug need
while :
do
	echo "Press [CTRL+C] to stop.."
	sleep 1
done


# WORKS ON DEV 

# poetry run python cgp_db/main_api.py

# gives:

#   File "/condorgp/cgp_db/main_api.py", line 7, in <module>
#     from cgp_db.database import SessionLocal
#   File "/condorgp/cgp_db/database.py", line 6, in <module>
#     engine = create_engine(DB_URL)
#              ^^^^^^^^^^^^^^^^^^^^^
#   File "<string>", line 2, in create_engine
#   File "/root/.cache/pypoetry/virtualenvs/condorgp-hQdFSJgI-py3.12/lib/python3.12/site-packages/sqlalchemy/util/deprecations.py", line 375, in warned
#     return fn(*args, **kwargs)
#            ^^^^^^^^^^^^^^^^^^^
#   File "/root/.cache/pypoetry/virtualenvs/condorgp-hQdFSJgI-py3.12/lib/python3.12/site-packages/sqlalchemy/engine/create.py", line 516, in create_engine
#     u, plugins, kwargs = u._instantiate_plugins(kwargs)
#                          ^^^^^^^^^^^^^^^^^^^^^^
# AttributeError: 'NoneType' object has no attribute '_instantiate_plugins'
