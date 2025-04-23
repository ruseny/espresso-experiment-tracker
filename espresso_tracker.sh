#!/bin/bash

# This script is used to launch first the backend and then the frontend
# of the espresso tracker application in the background, making sure 
# that they listen to the correct ports specified in the .env file.
# It is assumed that the conda environment named "espresso" already 
# exists and correctly configured.

current_dir="$(dirname "$0")"
source "${current_dir}/.env"

backend_path="${current_dir}/backend/main.py"
frontend_path="${current_dir}/frontend/main.py"

conda run -n espresso fastapi run \
    --host $BACKEND_HOST --port $BACKEND_PORT \
    $backend_path &
conda run -n espresso streamlit run \
    $frontend_path \
    --server.port $FRONTEND_PORT &