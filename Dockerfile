FROM ubuntu:21.04

RUN mkdir /api
RUN apt update; DEBIAN_FRONTEND=noninteractive apt install mariadb-server mariadb-client python3 python3-pip -y

COPY . /api
WORKDIR /api
RUN pip3 install -r requirements.txt

ENTRYPOINT [ "/bin/bash" ]
CMD ["./start.sh"]