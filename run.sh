#!/bin/bash

export FLASK_APP=gendemo
export FLASK_ENV=development
export FLASK_RUN_PORT=8002
flask run --host 0.0.0.0
