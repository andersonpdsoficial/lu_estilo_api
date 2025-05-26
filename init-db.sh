#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "postgres" <<-EOSQL
    DO \$\$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'lu_estilo') THEN
            CREATE DATABASE lu_estilo;
        END IF;
    END
    \$\$;
EOSQL