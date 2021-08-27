#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "postgres" <<-EOSQL
  CREATE DATABASE $DB_NAME;
  CREATE USER $DB_USER WITH ENCRYPTED PASSWORD '$DB_USER_PASSWORD';
  GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
  ALTER USER $DB_USER CREATEDB;

EOSQL



psql -v ON_ERROR_STOP=1 --username "$DB_USER" --dbname "$DB_NAME" <<-EOSQL


  ALTER ROLE $DB_USER SET client_encoding TO 'utf8';

  ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';

  ALTER ROLE $DB_USER SET timezone TO 'UTC';



  

EOSQL
