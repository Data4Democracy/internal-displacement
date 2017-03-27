#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE USER d4d WITH PASSWORD 'democracy';
    CREATE DATABASE id;
    GRANT ALL PRIVILEGES ON DATABASE id TO d4d;
EOSQL

psql -v ON_ERROR_STOP=1 --username "d4d" id < /schema.sql