#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE USER tester WITH PASSWORD 'tester';
    CREATE DATABASE id_test;
    GRANT ALL PRIVILEGES ON DATABASE id_test TO tester;
EOSQL

psql -v ON_ERROR_STOP=1 --username "tester" id_test < /schema.sql