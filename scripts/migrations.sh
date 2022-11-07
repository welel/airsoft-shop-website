#!/bin/bash
python ../shop/manage.py migrate
python ../shop/manage.py makemigrations user
python ../shop/manage.py migrate user
python ../shop/manage.py makemigrations main
python ../shop/manage.py migrate main
python ../shop/manage.py makemigrations shopping
python ../shop/manage.py migrate shopping