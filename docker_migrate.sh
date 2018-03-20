#!/usr/bin/env bash
cd zamsee-back
/etc/init.d/postgresql start
./manage.py migrate --noinput
./manage.py create_su