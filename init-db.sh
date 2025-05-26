#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "postgres" <<-EOSQL
    CREATE DATABASE lu_estilo;
    GRANT ALL PRIVILEGES ON DATABASE lu_estilo TO postgres;
EOSQL