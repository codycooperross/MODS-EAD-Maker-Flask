#!/bin/sh

export FLASK_APP=flask_app.py
export FLASK_ENV=development
export FLASK_DEBUG=1
python3 -m flask run