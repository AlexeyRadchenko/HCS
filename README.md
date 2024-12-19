## Overview

Servises for ....
[vue](https://github.com/vuejs/vue).

sudo -u postgres psql
postgres=# create user myuser with encrypted password 'mypass';
postgres=# create database users_control_db with owner PGmain_dbuser encoding UTF8 LC_COLLATE='ru_RU.UTF-8' LC_CTYPE='ru_RU.UTF-8';
postgres=# grant all privileges on database mydb to myuser;

create database accounts_db with owner pgmain_dbuser encoding UTF8 LC_COLLATE='ru_RU.UTF-8' LC_CTYPE='ru_RU.UTF-8' template template0;

api server upgrade cert 
```
sudo certbot certonly --force-renew --no-verify-ssl -d example.com

DJANGO_ENV=production gunicorn --bind 0.0.0.0:8000 myproject.wsgi:application

```
user www-data;
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;

events {
        worker_connections 768;
        # multi_accept on;
}

http {

        ##
        # Basic Settings
        ##

        sendfile on;
        tcp_nopush on;
        types_hash_max_size 2048;
        # server_tokens off;

        # server_names_hash_bucket_size 64;
        # server_name_in_redirect off;

        include /etc/nginx/mime.types;
        default_type application/octet-stream;

        
        ##
        # SSL Settings
        ##

        ssl_protocols TLSv1 TLSv1.1 TLSv1.2 TLSv1.3; # Dropping SSLv3, ref: POODLE
        ssl_prefer_server_ciphers on;

        ##
        # Logging Settings
        ##

        access_log /var/log/nginx/access.log;
        error_log /var/log/nginx/error.log;

        ##
        # Gzip Settings
        ##

        gzip on;

        # gzip_vary on;
        # gzip_proxied any;
        # gzip_comp_level 6;
        # gzip_buffers 16 8k;
        # gzip_http_version 1.1;
        # gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

        ##
        # Virtual Host Configs
        ##

        include /etc/nginx/conf.d/*.conf;
        include /etc/nginx/sites-enabled/*;
} 

https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-20-04  