#!/usr/bin/env bash
ENV_NAME=mantaray3
source activate $ENV_NAME
input_script="./ipython_scripts/s00_test_connections.py"
output_notebook="./jupyter_notebooks/s00_test_connections.py"
python -m py2jnb $input_script $output_notebook

