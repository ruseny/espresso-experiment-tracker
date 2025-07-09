#!/bin/bash

# This script is used to launch first the backend and then the frontend
# of the espresso tracker application in the background, making sure 
# that they listen to the correct ports specified in the .env file.
# It is assumed that the conda environment named "espresso" already 
# exists and correctly configured.

file_path="$(realpath "$0")"
current_dir="$(dirname "$file_path")"
source "${current_dir}/.env"

backend_path="${current_dir}/backend/main.py"
frontend_path="${current_dir}/frontend/main.py"

conda run -n espresso python $backend_path &
conda run -n espresso streamlit run \
    $frontend_path \
    --server.port $FRONTEND_PORT &
