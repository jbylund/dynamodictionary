FROM ubuntu:latest
RUN ln -s /bin/python3 /bin/python
RUN apt-get -y update > /dev/null
RUN apt-get install -y \
    git \
    lftp \
    openssh-client \
    coreutils \
    curl \
    python3-pip

RUN curl -sSL https://get.docker.com/ | sh
RUN python -m pip install --upgrade pip flake8 pytest
