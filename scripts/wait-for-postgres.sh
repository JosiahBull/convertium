#!/bin/sh
# wait-for-postgres.sh
# source: https://docs.docker.com/compose/startup-order/

set -e
<<<<<<< HEAD

=======

>>>>>>> 99cbb9a6d11708e8842070bab48b0776fe8b42f2
until PGPASSWORD="convertium" psql -h "postgres" -U "convertium" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done
<<<<<<< HEAD

=======

>>>>>>> 99cbb9a6d11708e8842070bab48b0776fe8b42f2
>&2 echo "Postgres is up - executing command"
exec "$@"
