#!/bin/bash
#cd /tmp/pycharm_project_700
echo "init project"
python3 init.py
echo "start web server"
nohup gunicorn wsgi:app -c gun.py >/dev/null 2>&1 &
