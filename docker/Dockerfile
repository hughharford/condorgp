# DOCKER_BUILDKIT=1 docker build --target=runtime -f docker/Dockerfile . 

# The builder image, used to build the virtual environment
FROM python:3.12-bullseye as builder

RUN pip install poetry==1.8.4

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /condorgp

COPY pyproject.toml poetry.lock ./

RUN touch README.md

RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

# The runtime image, used to just run the code provided its virtual environment
FROM python:3.12-slim-bullseye as runtime

ENV VIRTUAL_ENV=/condorgp/.venv \
    PATH="/condorgp/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY . ./condorgp

WORKDIR /condorgp

RUN pip install poetry 
RUN poetry install
#  && pip uninstall poetry

# create log folder and empty log file, for ease
# RUN mkdir /condorgp/condorgp/util/logs/ && \
RUN touch /condorgp/condorgp/util/logs/condor_log.txt

# create checkpoint folder and empty checkpoint file, for ease
# RUN mkdir /condorgp/condorgp/util/checkpoints/ && \
RUN    touch /condorgp/condorgp/util/checkpoints/first_strat_done.pkl


CMD ["/bin/bash"]
