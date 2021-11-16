#FROM ubuntu:21.04
FROM centos:7

RUN mkdir /api
#RUN apt update; DEBIAN_FRONTEND=noninteractive apt install mariadb-server mariadb-client python3 python3-pip -y
RUN yum install mariadb-server mariadb python3 python3-pip -y
RUN mysql_install_db --user=mysql

RUN sed -i '/\[mysqld\]/aport=3306' /etc/my.cnf

RUN \
  echo "/usr/bin/mysqld_safe --basedir=/usr &" > /tmp/config && \
  echo "cat /var/log/mariadb/mariadb.log" >> /tmp/config && \
  echo "mysqladmin --silent --wait=30 ping || exit 1" >> /tmp/config && \
  echo "mysql -e 'GRANT ALL PRIVILEGES ON *.* TO \"root\"@\"%\";'" >> /tmp/config && \
  bash /tmp/config && \
  rm -f /tmp/config

COPY . /api
WORKDIR /api
RUN pip3 install -r requirements.txt

ENTRYPOINT [ "/bin/bash" ]
CMD ["./start.sh"]