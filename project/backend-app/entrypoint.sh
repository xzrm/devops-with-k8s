#!/bin/sh

if [ "$CLEAN_DB" = "true" ]
then
    echo "creating new db"
    python manage.py create_db
fi

exec "$@"