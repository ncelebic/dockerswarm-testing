#!/bin/bash -i

virtualenv ./venv
source ./venv/bin/activate
pip install -U setuptools
pip install -r py.req
