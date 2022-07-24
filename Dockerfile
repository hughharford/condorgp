FROM ubuntu:20.04

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
# NOT INCLUDED WITH UBUNTU_20.04
#
# git

# was: RUN apt-get install docker.io -y
RUN apt-get install -y docker.io docker-compose


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


############# Then, PYTHON 3.8.0 #########################################################
# ''''''''''''''' ############################# '''''''''''''''''' ####################

ENV PYTHON_VERSION 3.8.0

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
ENV PYTHON_PIP_VERSION 21.0.0
# https://github.com/docker-library/python/issues/365
ENV PYTHON_SETUPTOOLS_VERSION 57.0.0
# https://github.com/pypa/get-pip
ENV PYTHON_GET_PIP_URL https://github.com/pypa/get-pip/raw/3cb8888cc2869620f57d5d2da64da38f516078c7/public/get-pip.py
ENV PYTHON_GET_PIP_SHA256 c518250e91a70d7b20cceb15272209a4ded2a0c263ae5776f129e0d9b5674309

# HSTH additional to deal with: WARNING: pip is configured with locations that require TLS/SSL, however the ssl module in Python is not available.
RUN apt-get install -y libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev

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

# CondorGP clone lean
RUN git clone https://github.com/QuantConnect/Lean.git
WORKDIR /Lean/
# RUN pip install Lean # requires a "Y"
# RUN lean init
WORKDIR /condorgp/

# HSTH - CondorGP files copy over
# COPY Lean/ Lean/ # doesn't work as Lean includes .dockerignore
COPY condorgp/ condorgp/
COPY leanQC/ leanQC/
COPY tests/ tests/
COPY setup.py setup.py

# HSTH fulfill from requirements.txt
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

CMD ["/bin/bash"]
