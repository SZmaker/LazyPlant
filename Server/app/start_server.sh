#!/bin/bash

LISTEN_PORT=20002

nohup gunicorn app.wsgi -b :$LISTEN_PORT > dev.log &
echo $! > .pid_gunicorn
