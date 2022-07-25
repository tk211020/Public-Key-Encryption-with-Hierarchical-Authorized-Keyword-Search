FROM debian:10

RUN apt update -y
RUN apt-get install \
    gcc \
    vim \
    wget \
    xz-utils \
    subversion \
    python3 \
    python3-setuptools python3-dev python3-matplotlib \
    libgmp-dev \
    gzip \
    m4 \
    flex \
    bison \
    make \
    git \
    libssl-dev \
    -y

RUN wget https://gmplib.org/download/gmp/gmp-6.2.1.tar.xz && \
    tar Jxvf gmp-6.2.1.tar.xz && \
    cd gmp-6.2.1 && \
    ./configure && \
    make && \
    make check install

RUN wget https://crypto.stanford.edu/pbc/files/pbc-0.5.14.tar.gz && \
    tar xvf pbc-0.5.14.tar.gz && \
    cd pbc-0.5.14 && \
    ./configure && \
    make && \
    make install

RUN git clone https://github.com/JHUISI/charm.git && \
    cd charm && \
    ./configure.sh && \
    make && \
    make install && \
    rm -rf charm

WORKDIR /usr/etc

ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib 

RUN echo 'alias build="gcc main.c -L. -lpbc -lgmp -I /usr/local/include/pbc"' >> ~/.bashrc
RUN echo 'alias debug="gcc -DDEBUG main.c -L. -lpbc -lgmp -I /usr/local/include/pbc"' >> ~/.bashrc
RUN echo 'alias run="./a.out < /usr/etc/pbc-0.5.14/param/a.param"' >> ~/.bashrc

WORKDIR /usr/src


CMD ["sleep", "infinity"]