#!/bin/sh
# wait-for-postgres.sh
# source: https://docs.docker.com/compose/startup-order/

set -e
  
until PGPASSWORD="convertium" psql -h "postgres" -U "convertium" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done
  
>&2 echo "Postgres is up - executing command"
exec "$@"
