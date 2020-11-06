#
# A dev environment for rimu-py
#
FROM python:3.8-slim
WORKDIR /rimu-py

# Install dev packages.
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --requirement requirements.txt
RUN apt-get update && \
    apt-get install --no-install-recommends --yes make && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# If UID is non-zero create a user with uid=$UID and gid=$GID.
ARG UID=${UID:-0}
ARG GID=${GID:-0}
RUN if [ $UID -eq 0 ]; then exit; fi && \
    groupadd -g $GID user && \
    useradd -m -u $UID -g $GID user

# Add per container anonymous volumes for volatile cache directories.
RUN mkdir /rimu-py/.mypy_cache /rimu-py/.pytest_cache && \
    if [ $UID -eq 0 ]; then exit; fi && \
    chown $UID:$GID /rimu-py/.mypy_cache /rimu-py/.pytest_cache
VOLUME /rimu-py/.mypy_cache
VOLUME /rimu-py/.pytest_cache

USER $UID
CMD echo This image should be executed with the docker-compose run command.