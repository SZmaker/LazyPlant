#!/bin/bash

read proc < .pid_gunicorn
kill -9 $proc
