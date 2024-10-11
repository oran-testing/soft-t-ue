FROM ubuntu:22.04

ENV CONFIG="./configs/zmq/ue_zmq.conf"
ENV ARGS=""
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y \
    cmake \
    make \
    gcc \
    g++ \
    pkg-config \
    libfftw3-dev \
    libmbedtls-dev \
    libsctp-dev \
    libyaml-cpp-dev \
    libgtest-dev \
    libzmq3-dev \
    net-tools \
    libboost-all-dev \
    libconfig++-dev \
    iperf3 \
    git \
    libxcb-cursor0 \
    libgles2-mesa-dev \
    gr-osmosdr \
    python3 \
    python3-pip && \
    pip3 install kivy kivy_garden.graph

WORKDIR /opt

RUN git clone https://github.com/oran-testing/soft-t-ue && mkdir -p ./soft-t-ue/build

WORKDIR /opt/soft-t-ue/build
RUN cmake ../ && \
    make -j$(nproc) && \
    make install && \
    srsran_install_configs.sh user && \
    ldconfig

WORKDIR /opt/soft-t-ue/

CMD /usr/local/bin/srsue "${CONFIG}" $ARGS
