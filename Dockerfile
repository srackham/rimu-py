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

# Install user with host user UID and GID.
ARG UID
ARG GID
ARG USER=user
ARG GROUP=user
RUN : "${UID:?Build argument UID needs to be set to host user ID}" && \
    : "${GID:?Build argument GID needs to be set to host group ID}" && \
    groupadd -g $GID $GROUP && \
    useradd -m -u $UID -g $GID $USER

# Add per container anonymous volumes for volatile cache directories.
RUN mkdir /rimu-py/.mypy_cache /rimu-py/.pytest_cache && \
    chown $USER:$GROUP /rimu-py/.mypy_cache /rimu-py/.pytest_cache
VOLUME /rimu-py/.mypy_cache
VOLUME /rimu-py/.pytest_cache

USER $USER
CMD echo This image should be executed with the docker-compose run command.