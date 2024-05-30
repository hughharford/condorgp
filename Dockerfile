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
# ALREADY INSTALLED WITH UBUNTU_20.04
#			Document viewer - for pdf
#			SNAP
#			GIT
#
# NOT INCLUDED WITH UBUNTU_20.04
#
# so install manually once set up, or?

#		VS Code
#
# Further useful:
#
#  FROM get-pip.py (see below and: https://github.com/pypa/get-pip)
#		wheel
#		setuptools
#		pip
#
#	NOTE how more complex get-pip.py with specific versions is sidestepped below


# was: RUN apt-get install docker.io -y
RUN apt-get install -y docker.io docker-compose

# THESE FEEL SUPERFLUOUS 240523
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

#### LE WAGON INSTALLS ##### start #
# REF                                https://gto76.github.io/python-cheatsheet/
### TODO: Convert to requirements.txt

# RUN pip3 install pygame \
	# && pip3 install PySimpleGUI \
	# # FROM 					REF/#logging
	# && pip3 install loguru \
	# # for logging
	# && pip3 install requests beautifulsoup4 \
	# # for web-scraping
	# && pip3 install bottle \
	# # for web
	# && pip3 install line_profiler memory_profiler \
	# # for profiling by line
	# && pip3 install pycallgraph2 \
	# # for a PNG image of the call graph with highlighted bottlenecks (see example)
	# && pip3 install pillow \
	# # for image
	# && pip3 install pyttsx3 \
	# # for text to speech recognition
	# #													&& pip3 install simpleaudio \
	# # for synthesizer
	# && pip3 install plotly kaleido \
	# # for plotly
	# && pip3 install cython \
	# # for the Library that compiles Python code into C.
	# && pip3 install tqdm \
	# # progress bar
	# && pip3 install tabulate
	# # can prints a CSV file as an ASCII table

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
############# @@@@@@@@@@@@@@@ #########################################################
# ''''''''''''''' ############################# '''''''''''''''''' ####################
############# @@@@@@@@@@@@@@@ #########################################################
# ''''''''''''''' ############################# '''''''''''''''''' ####################

# HSTH additional to deal with: 
  # WARNING: pip is configured with locations that require TLS/SSL, 
  # however the ssl module in Python is not available.
RUN apt-get install -y \
#  libreadline-gplv2-dev \  
# TO DO: Need to understand why there was no candidate for libreadline-gplv2-dev 
# and why it didn't matter on previous builds
  libncursesw5-dev \
  libssl-dev \
  libsqlite3-dev \
  tk-dev \
  libgdbm-dev \
  libc6-dev \
  libbz2-dev

############# Then, PYTHON #########################################################
# ''''''''''''''' ############################# '''''''''''''''''' ####################

# WAS 3.8.0 (builds successfully) we want: 3.10.6
ENV PYTHON_VERSION 3.10.6

RUN set -ex \
	\
	&& wget -O python.tar.xz "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz" \
	&& wget -O python.tar.xz.asc "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz.asc" \
	&& mkdir -p /usr/src/python \
	&& tar -xJC /usr/src/python --strip-components=1 -f python.tar.xz \
	&& rm python.tar.xz \
	\
	&& cd /usr/src/python \
	&& gnuArch="$(dpkg-architecture --query DEB_BUILD_GNU_TYPE)" \
	&& ./configure \
		--build="$gnuArch" \
		--enable-loadable-sqlite-extensions \
		--enable-optimizations \
		--enable-option-checking=fatal \
		--enable-shared \
		--with-lto \
		--with-system-expat \
		--with-system-ffi \
		--without-ensurepip \
	&& make -j "$(nproc)" \
	&& make install \
	&& rm -rf /usr/src/python \
	\
	&& find /usr/local -depth \
		\( \
			\( -type d -a \( -name test -o -name tests -o -name idle_test \) \) \
			-o \( -type f -a \( -name '*.pyc' -o -name '*.pyo' -o -name '*.a' \) \) \
		\) -exec rm -rf '{}' + \
	\
	&& ldconfig \
	\
	&& python3 --version

############# @@@@@@@@@@@@@@@ #########################################################
# ''''''''''''''' ############################# '''''''''''''''''' ####################
############# @@@@@@@@@@@@@@@ #########################################################
# ''''''''''''''' ############################# '''''''''''''''''' ####################
############# PYTHON VERSIONS #########################################################
# ''''''''''''''' ############################# '''''''''''''''''' ####################

# if this is called "PIP_VERSION", pip explodes with "ValueError: invalid truth value '<VERSION>'"
# was 20.0.0:
ENV PYTHON_PIP_VERSION 22.2.1
# https://github.com/docker-library/python/issues/365
ENV PYTHON_SETUPTOOLS_VERSION 57.0.0
# https://github.com/pypa/get-pip
ENV PYTHON_GET_PIP_URL https://github.com/pypa/get-pip/raw/3cb8888cc2869620f57d5d2da64da38f516078c7/public/get-pip.py
ENV PYTHON_GET_PIP_SHA256 c518250e91a70d7b20cceb15272209a4ded2a0c263ae5776f129e0d9b5674309


RUN set -ex; \
	\
	curl -sSL https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
	python get-pip.py \
	pip --version; \
	\
	find /usr/local -depth \
		\( \
			\( -type d -a \( -name test -o -name tests -o -name idle_test \) \) \
			-o \
			\( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) \
		\) -exec rm -rf '{}' +; \
	rm -f get-pip.py


# NEED TO INVESTIGATE HOW TO SET UP SSH KEY AUTOMATICALLY
# - better:
#   echo -e "Host github.com
#       Hostname github.com                            
#       User git                  
#       IdentityFile '~/.ssh/some_key'" > ~/temp_config_example.txt
  
#       ssh -T git@github.com
#       Hi hughharford! You've successfully authenticated, but GitHub does not provide shell access.
  
#   - Make sure an SSH key is setup with Github on this instance, then:
#   mkdir code; cd code
  
  
#   ### dotfiles
#   export GITHUB_USERNAME=`gh api user | jq -r '.login'`
#   echo $GITHUB_USERNAME
#   cd ~/code; git clone git@github.com:hughharford/dotfiles.git
#   cd ~/code/dotfiles && zsh install.sh
#   cd ~/code/dotfiles && zsh git_setup.sh

# additional 24 05 23 quickly
RUN pip3 install -y gh \
  make 

RUN git clone https://github.com/pyenv/pyenv.git ~/.pyenv \
  exec zsh

# additional 24 05 23 quickly 2
RUN sudo apt install -y curl git imagemagick jq unzip vim zsh tree; \
  sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"; \
  sudo apt-get update; sudo apt-get install direnv; \
  echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc;

# further python support packages?
RUN sudo apt-get update; sudo apt-get install make build-essential libssl-dev zlib1g-dev \
  libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
  libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev \
  python3-dev

### set virtual environment
RUN git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv \
  exec zsh \
  pyenv virtualenv 3.10.6 condorgp \
  pyenv global condorgp

# HSTH fulfill from requirements.txt
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

CMD ["/bin/bash"]
