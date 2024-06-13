# from:
  # /home/hughharford/code/hughharford/condorgp/docs/docker_files_ref/Dockerfile_working_basic_220724
  # built fine 240522
  # trying version updates 

# NB! this:
  #
# NOTE: THIS DOCKERFILE IS GENERATED VIA "update.sh"
#		 ORIGINALLY MS VSCODE dockerfile for dev in container work
# PLEASE DO NOT EDIT IT DIRECTLY.

# NOTES ##  ##  ## see likely useful ref:
#										https://github.com/fcwu/docker-ubuntu-vnc-desktop
#

# was ubuntu:20.04 
FROM ubuntu:22.04 

# ensure local python is preferred over distribution python
ENV PATH /usr/local/bin:$PATH

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8

# these get set in zsh but cause local error
# ENV LANG=en_US.UTF-8
# ENV LC_ALL=en_US.UTF-8

# set location to avoid hang on tzdata
ENV TZ=Europe/London
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update

# extra dependencies (over what base already includes, was buildpack-deps, now ubuntu:20.04)
RUN apt-get update && apt-get install -y --no-install-recommends \
		apt-utils \
		libbluetooth-dev \
		tk-dev \
		uuid-dev \
	&& rm -rf /var/lib/apt/lists/*

# standard issue update && ...
RUN apt-get update && apt-get install -y apt-transport-https

# HSTH: STEPS to install a few extras
RUN apt-get install -y \
		unzip \
		curl \
		wget \
		virtualenv \
		python3-pip

######
######
#		INSTALL NOTES
######
######
#

### TODO: Convert to requirements.txt
#### LE WAGON INSTALLS ##### end #

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# # make some useful symlinks that are expected to exist
 RUN cd /usr/local/bin \
 	&& ln -s idle3 idle \
 	&& ln -s pydoc3 pydoc \
 	&& ln -s python3 python \
 	&& ln -s python3-config python-config

############# PYTHON #########################################################
# ''''''''''''''' ############################# '''''''''''''''''' ####################

# HSTH additional to deal with: 
  # WARNING: pip is configured with locations that require TLS/SSL, 
  # however the ssl module in Python is not available.

RUN apt-get install -y \
#  libreadline-gplv2-dev \  
# TO DO: 250519 Need to understand why there was no candidate for libreadline-gplv2-dev 
# and why it didn't matter on previous builds
  libgdbm-dev libc6-dev libbz2-dev

# further python support packages? MOVED BEFORE PYTHON VERSION
RUN apt-get update; apt-get install -y make build-essential libssl-dev zlib1g-dev \
  libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
  libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev \
  python3-dev libncurses5-dev git

############# Then, PYTHON #####################################################
# ''''''''''''''' ############################# '''''''''''''''''' ####################
WORKDIR /home/user

# install pyenv
RUN git clone https://github.com/pyenv/pyenv.git .pyenv
ENV HOME  /home/user
ENV PYENV_ROOT $HOME/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH
RUN echo 'export PYENV_ROOT="$HOME/.pyenv"' >> .bashrc
RUN echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> .bashrc
RUN echo 'eval "$(pyenv init -)"' >> .bashrc
RUN pyenv install 3.10.12

# install pyenv-virtualenv
RUN git clone https://github.com/yyuu/pyenv-virtualenv.git .pyenv/plugins/pyenv-virtualenv
RUN echo 'eval "$(pyenv virtualenv-init -)"' >> .bashrc

# # NEED THESE
RUN pip3 install numpy setuptools wheel six auditwheel setuptools


############# PYTHON #########################################################
# ''''''''''''''' ############################# '''''''''''''''''' ####################

ENV PYTHON_PIP_VERSION 22.2.1
# https://github.com/docker-library/python/issues/365
ENV PYTHON_SETUPTOOLS_VERSION 70.0.0
# was 57.0.0 
# SETUPTOOLS version 70 indicated: https://pypi.org/project/setuptools/#history
# https://github.com/pypa/get-pip
ENV PYTHON_GET_PIP_URL https://github.com/pypa/get-pip/raw/3cb8888cc2869620f57d5d2da64da38f516078c7/public/get-pip.py
ENV PYTHON_GET_PIP_SHA256 c518250e91a70d7b20cceb15272209a4ded2a0c263ae5776f129e0d9b5674309

# additional 24 05 23 quickly 2
RUN apt install -y curl git imagemagick jq unzip vim zsh tree gh make; \
  sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"; \
  apt-get update; apt-get install direnv; \
  echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc;

# again to go past issues:
RUN pip3 install --ignore-installed six

# install nautilus_trader
# git clone first
RUN mkdir $HOME/code/
RUN mkdir $HOME/code/nautilus_trader
# CONSIDER git shallow clone to speed up
# use --single-branch
# WORKS: much much faster
RUN git clone --single-branch https://github.com/nautechsystems/nautilus_trader.git $HOME/code/nautilus_trader
WORKDIR $HOME/code/nautilus_trader

# setup pyenv, but deactivate after as build.py does it's own:  
RUN pyenv virtualenv 3.10.12 naut_trader
# # RUN pyenv activate naut_trader # not in a Dockerfile
RUN . /home/user/.pyenv/versions/naut_trader/bin/activate

# ACTIVATING VENV FOR EACH LINE:
# install nautilus_trader dependencies
# clang
RUN apt install -y clang
# rust
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
ENV PATH=${PATH}:$HOME/.cargo/bin
# this didn't work:  RUN . $HOME/.cargo/env

# poetry
RUN . /home/user/.pyenv/versions/naut_trader/bin/activate && \
    curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/home/user/.local/bin:$PATH"

RUN . /home/user/.pyenv/versions/naut_trader/bin/activate && \
    pip3 install toml Cython requests numpy

RUN . /home/user/.pyenv/versions/naut_trader/bin/activate && \
    poetry run python build.py

# GOT TO HERE SUCCESSFULLY 24 06 12 1430

# # # skip these, for working within repo... unlikely
# # RUN pip install pre-commit
# # RUN pre-commit install

# WORKDIR $HOME/code/
# # install condorgp
WORKDIR $HOME/code/
RUN pyenv virtualenv 3.10.12 condorgp
# RUN pyenv activate condorgp # not in a Dockerfile
RUN git clone --single-branch https://github.com/hughharford/condorgp.git 
WORKDIR $HOME/code/condorgp
RUN . /home/user/.pyenv/versions/naut_trader/bin/activate && \
    make install

# GOT TO HERE SUCCESSFULLY 24 06 12 2104

### 24 06 13 - somehow got past nautilus_trader imports, and ones unused
### and then got to pika AQMP failed connection failure. 
### This clearly indicates that the lack of port or whatever was the fault
### i.e. not the nautilus and condorgp pyenv interaction.
###
### Trouble being, on each container the record is gone quick of what was
### tried so it can be repeated. Ouch. 

### these were likely involved. overall, make sure to make a record of actions 
### taken until the same result is seen(!) Wow, really?!

### 1stly, start from a fresh container, 
### starts in ~/code/condorgp with (condorgp):
pyenv versions
. /home/user/.pyenv/versions/naut_trader/bin/activate
make install (i.e. install condorgp)
# try:
python condorgp/comms/run_condorgp/condor_worker.py
# result: No module named 'nautilus_trader'
cd ../nautilus_trader
poetry run python build.py
# very short Nautilus Builder 11.05 seconds
cd ../condorgp
# same as above
# result: No module named 'nautilus_trader'
# CHECK PYTHON IMPORTS
# @: (naut_trader) root@3e0f61e222fd:~/code/condorgp# 
# NOTE:
  # Python 3.10.12 (main, Jun 12 2024, 13:13:03) [GCC 11.4.0] on linux
  # Type "help", "copyright", "credits" or "license" for more information.
  # >>> import nautilus_trader
  # Traceback (most recent call last):
  #   File "<stdin>", line 1, in <module>
  # ModuleNotFoundError: No module named 'nautilus_trader'
  # >>> import condorgp
  # >>> {i.e. imports fine}
# cd ../nautilus_trader
# (naut_trader) root@3e0f61e222fd:~/code/nautilus_trader# python
# Python 3.10.12 (main, Jun 12 2024, 13:13:03) [GCC 11.4.0] on linux
# Type "help", "copyright", "credits" or "license" for more information.
# >>> import nautilus_trader
# >>> import condorgp
# >>> 
# TRY:
python ../condorgp/condorgp/comms/run_condorgp/condor_worker.py
# SAME ERROR AS ABOVE
# result: No module named 'nautilus_trader'
# TRY:
  pyenv global naut_trader
  pip freeze 
  # shows deap, pandas, pika, condorgp but not nautilus.
# TRY:
  poetry run python build.py
  # quick build again
  pip freeze 
  # still not showing nautilus_trader
# TRY:
  pip install -U nautilus_trader
  # shows:
#    Installing collected packages: uvloop, tqdm, pyarrow, msgspec, fsspec, nautilus_trader
# some of these were individually installed on the last succesful run, think so?
# NOW, progress, onto Ticker import failure:
#   from nautilus_trader.model.data import Ticker
# ImportError: cannot import name 'Ticker' from 'nautilus_trader.model.data' etc etc

# # #   ### dotfiles
# WORKDIR $HOME/code/
# RUN git clone https://github.com/hughharford/dotfiles.git
# WORKDIR $HOME/code/dotfiles
# RUN zsh install.sh

# FROM HERE NONE OF THIS IS CURRENT >>> # FROM HERE NONE OF THIS IS CURRENT >>> 
# FROM HERE NONE OF THIS IS CURRENT >>> # FROM HERE NONE OF THIS IS CURRENT >>> 

RUN apt install net-tools

ENV PATH="/usr/local/lib/python3.10/dist-packages:$PATH" 
ENV PYTHONPATH="/usr/local/lib/python3.10/dist-packages:$PYTHONPATH"

# 5672 already in use on host
EXPOSE 5673 
EXPOSE 15672

# for -it interactive running
CMD ["/bin/bash"]

# attempting command run
# CMD ["python3", "code/condorgp/comms/run_condorgp/condor_worker.py"]
