#!/bin/sh

# Run Flask CLI commands to create tables
python manage.py create_and_populate_tables_if_not_exist

# Start Flask app
flask run --host=0.0.0.0
