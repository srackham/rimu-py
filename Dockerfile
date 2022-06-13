# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# VSC Remote Containers default project source code location.
ARG PROJECT_DIR=/workspaces/rimu-py
ENV PYTHONPATH=${PROJECT_DIR}/src

# Install Ubuntu packages
RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y git sudo

# Enable passwordless sudo logins
# https://stackoverflow.com/a/65434659/1136455
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# Install pip requirements
RUN pip install --upgrade pip
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Use the default VSC Remote Containers working directory.
WORKDIR ${PROJECT_DIR}
COPY . ${PROJECT_DIR}

# Creates a non-root user with an explicit UID and adds permission to access the project folder
# https://code.visualstudio.com/remote/advancedcontainers/add-nonroot-user#_creating-a-nonroot-user
RUN adduser --uid 5678 --disabled-password --gecos "" appuser && chown -R appuser ${PROJECT_DIR}
# Allow user to sudo
RUN usermod -aG sudo appuser
# Set user password
RUN echo "appuser:appuser" | chpasswd
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["/usr/bin/make", "clean","test"]