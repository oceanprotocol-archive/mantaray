#!/usr/bin/env bash
ENV_NAME=mantaray3
source activate $ENV_NAME
input_script="./ipython_scripts/check_aws_s3.py"
output_notebook="./jupyter_notebooks/check_aws_s3.py"
python -m py2jnb $input_script $output_notebook

