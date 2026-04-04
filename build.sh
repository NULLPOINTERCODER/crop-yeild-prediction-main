#!/bin/bash
# Exit on any error
set -e

echo "--- Installing Dependencies ---"
# Using --break-system-packages because Vercel's build environment is externally managed (PEP 668)
python3 -m pip install -r requirements.txt --break-system-packages --no-cache-dir

echo "--- Running Migrations ---"
# Note: Migrations applied to the database configured via DATABASE_URL
python3 manage.py migrate --noinput

echo "--- Collecting Static Files ---"
python3 manage.py collectstatic --noinput --clear

echo "--- Build Finished ---"
