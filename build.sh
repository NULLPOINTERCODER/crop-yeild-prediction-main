#!/bin/bash
# Exit on any error
set -e

echo "--- Installing Dependencies ---"
pip install -r requirements.txt

echo "--- Running Migrations ---"
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

echo "--- Collecting Static Files ---"
# Collect static files into the directory specified in STATIC_ROOT (staticfiles_build)
python3 manage.py collectstatic --noinput --clear

echo "--- Build Finished ---"
