FROM ubuntu:16.04
RUN apt-get -y update && apt-get -y upgrade 
RUN apt-get install -y apt-utils 
RUN apt-get install -y wget 
RUN apt-get install -y bzip2
RUN wget https://downloads.getmonero.org/linux64
RUN bzip2 -d linux64
RUN tar xvf linux64.out
RUN ./monero-x86_64-linux-gnu-v0.17.2.0/monerod --detach
