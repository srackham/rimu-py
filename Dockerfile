FROM python:3.8-slim
WORKDIR /rimu-py
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --requirement requirements.txt
RUN apt-get update && \
    apt-get install --no-install-recommends --yes make && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN groupadd -g 1001 rimu && useradd -m -u 1001 -g rimu rimu

# Add per container anonymous volumes for volatile cache directories.
RUN mkdir /rimu-py/.mypy_cache /rimu-py/.pytest_cache && \
    chown rimu: /rimu-py/.mypy_cache /rimu-py/.pytest_cache
VOLUME /rimu-py/.mypy_cache
VOLUME /rimu-py/.pytest_cache

USER rimu
CMD sleep infinity