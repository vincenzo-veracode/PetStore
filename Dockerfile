FROM ubuntu:20.04


RUN apt-get update; DEBIAN_FRONTEND=noninteractive apt-get install -y apt-utils 
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y mariadb-server mariadb-client python3 python3-pip
#   systemctl ??

RUN mkdir /api
COPY . /api
WORKDIR /api
RUN chmod +x ./start.sh
RUN pip3 install -r requirements.txt

EXPOSE 5000

#ENTRYPOINT [ "/bin/bash" ]
#CMD ["./start.sh"]
ENTRYPOINT [ "./start.sh" ]
