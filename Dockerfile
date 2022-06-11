# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Project source code.
ENV PYTHONPATH=/workspaces/rimu-py/src

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

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
RUN adduser --uid 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
# Allow user to sudo
RUN sudo usermod -aG sudo appuser
# Set user password
RUN echo "appuser:appuser" | chpasswd
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["make", "clean","test"]