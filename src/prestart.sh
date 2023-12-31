#!/bin/bash

echo "Waiting for postgres connection"

while ! nc -z db 5432; do
    sleep 0.1
done

echo "PostgreSQL started"

while ! nc -z kafka 9092; do
    sleep 0.1
done

exec "$@"
