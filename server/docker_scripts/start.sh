#!/bin/bash

pip install --upgrade pip
pip install -r reqs/all.txt

export MYSQL_PASS=easykrishi
mysql -u root -h easykrishi_database -p$MYSQL_PASS < /scripts/mysql_initialize.sql

unlink /etc/nginx/sites-enabled/nginx_docker_easykrishi.config
ln -s /server/config_templates/nginx_docker_easykrishi.config /etc/nginx/sites-enabled/nginx_docker_easykrishi.config 
service nginx restart

fab deploy:easykrishi,easikrishi_pwd,easykrishi

while true; do sleep 1000 ; done
