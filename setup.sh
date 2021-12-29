#!/bin/bash

rm -rf conda_env
rm -rf venv
rm -rf __pycache__
conda env create --prefix ./conda_env --file environment.yml
source ./activate_env.sh