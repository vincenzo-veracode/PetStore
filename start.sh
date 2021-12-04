#!/bin/bash

#/etc/init.d/mariadb start &
/usr/bin/mysqld_safe --basedir=/usr &
sleep 5
mysqladmin --silent --wait=30 ping || exit 1
mysql -e 'GRANT ALL PRIVILEGES ON *.* TO "root"@"%";'
mysql -e "CREATE DATABASE flask_api;"
mysql -e "CREATE USER 'petstore'@'localhost' IDENTIFIED BY 'Ver@c0de';"
mysql -e "GRANT ALL ON *.* TO 'petstore'@'localhost';"
mysql -e "flush privileges;"

# this while/true loop *should* not be necessary with the switch to 'debug=False' 
# in the flask app, but better safe than sorry
while true; do
    python3 api.py
done
