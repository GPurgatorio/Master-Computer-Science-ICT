#!/bin/bash

redis-server /usr/local/etc/redis.conf &

python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
python setup.py develop

celery -A ReactionsService.tasks worker -B --loglevel=info &

python -m flask run
