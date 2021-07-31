#!/bin/sh

# POSTGRES DB PREP // unused but keeping for ref
if [ "$DATABSE" = "postgres"]; then
    echo "Waiting for postgres..."

    while ! nc -z $DATABSE_HOST $DATABSE_PORT; do
    sleep 0.1
    done

    echo "PostgreSQL has started"
fi

# Make migrations and migrate the database
echo "Making migrations..."
python manage.py makemigrations main --noinput
echo "Migrating the database..."
python manage.py migrate --noinput
exec "$@"