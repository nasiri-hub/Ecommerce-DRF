#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
python3 manage.py migrate 

# Collect statics
echo "Collecting static files"
python3 manage.py collectstatic --no-input

# Start server
echo "Starting server"
gunicorn --bind 0.0.0.0:8000 --workers 3 ecommerce.wsgi:application

