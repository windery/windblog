#!/bin/bash

source venv/bin/activate
./manage.py runserver -b 0.0.0.0:80 -w 5
