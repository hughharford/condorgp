#!/bin/bash

if $LOCAL_BASE_PATH = ""; then
	echo "local path set as: " $LOCAL_BASE_PATH
	echo "path set ok, assuming environment variables setup."
else
	echo "Looks as though your environment variables aren't set up. Attempting now."
	if [ -f .env ]; then echo .env present; else echo .env is missing;  fi;
	if [ -f .envrc ]; then echo .envrc present; else echo .envrc is missing; fi;
	sudo apt install direnv
  make update_env
fi
