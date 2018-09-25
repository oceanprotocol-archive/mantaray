#!/usr/bin/env bash
input_script="./ipython_scripts/s00_test_connections.py"
output_notebook="./jupyter_notebooks/s00_test_connections.py"
python -m py2nb $input_script $output_notebook

