#!/bin/bash
# Exit on any error
set -e

echo "--- Installing Dependencies ---"
python3 -m pip install -r requirements.txt

echo "--- Running Migrations ---"
# Note: Migrations should be generated locally and committed to Git
# This only applies pending migrations to the database
python3 manage.py migrate --noinput

echo "--- Collecting Static Files ---"
python3 manage.py collectstatic --noinput --clear

echo "--- Build Finished ---"
