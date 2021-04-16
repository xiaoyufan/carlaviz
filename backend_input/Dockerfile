FROM ubuntu:18.04

RUN apt update \
    && apt install -y software-properties-common \
        python3-pip \
        libxerces-c3.2 \
    && apt install -y python3.7 \
    && apt install -y python3.7-venv \
    && python3.7 -m pip install pip

RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 1AF1527DE64CB8D9 && \
    add-apt-repository "deb [arch=amd64] http://dist.carla.org/carla $(lsb_release -sc) main" && \
    apt update && \
    apt install -y carla-simulator=0.9.10-1

ENV PYTHONPATH="/opt/carla-simulator/PythonAPI/carla/dist/carla-0.9.10-py3.6-linux-x86_64.egg"

RUN python3.7 -m venv /opt/venv
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

COPY requirements.txt requirements.txt
RUN python3.7 -m pip install -r requirements.txt

ENV SERVER_IP localhost
ENV SERVER_PORT 13254
ENV CARLA_SERVER_IP localhost
ENV CARLA_SERVER_PORT 2000

COPY . .

CMD python3.7 /app/main.py \
        --server-host $SERVER_IP \
        --server-port $SERVER_PORT \
        --carla-host $CARLA_SERVER_IP \
        --carla-port $CARLA_SERVER_PORT
