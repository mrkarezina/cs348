#!/bin/sh

# Run Flask CLI commands to create tables
python manage.py run_all_scripts_with_check

# Start Flask app
flask run --host=0.0.0.0
