#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE USER jupyter WITH PASSWORD 'jupyter';
    CREATE USER nodejs WITH PASSWORD 'nodejs';
    CREATE DATABASE id;
    GRANT ALL PRIVILEGES ON DATABASE id TO jupyter;
    GRANT ALL PRIVILEGES ON DATABASE id TO nodejs;
EOSQL