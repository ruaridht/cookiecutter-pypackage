FROM registry.hub.docker.com/library/python:3.10-slim-bullseye AS devcontainer

RUN apt update && apt upgrade -y
RUN apt install -y git

RUN python -m pip install --upgrade pip
RUN pip install poetry

ADD .config/pypoetry/config.toml /root/.config/pypoetry/config.toml

LABEL author="Ruaridh Thomson"
LABEL version="20230610"