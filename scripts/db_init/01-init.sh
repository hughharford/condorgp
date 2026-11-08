#!/bin/bash
# Postgres first-boot initialisation.
#
# Mounted at /docker-entrypoint-initdb.d/ by:
#   - Kubernetes: ConfigMap "cgp-db-init" in k8s/04-postgres.yaml
#   - Docker Compose: docker_compose/docker-compose-db-graf-rmq.yml
# KEEP THE TWO IN SYNC: the ConfigMap holds a copy of this file.
#
# The official postgres image runs these scripts ONLY when the data directory
# is empty (first start of a fresh volume). Changing this file does not alter an
# existing database; to re-run it, delete the PVC / volume (this destroys data).
#
# Required environment (supplied from the cgp-secrets Secret / cgp-config):
#   APP_DB_USER  application role to create
#   APP_DB_PASS  its password
#   APP_DB_NAME  application database (created if missing, owned by that role)
#
# The image creates $POSTGRES_DB itself before running this script. In this repo
# POSTGRES_DB and APP_DB_NAME are the same name, so the database usually EXISTS by
# now: the script creates it only if it is missing, and then hands it to the
# application role either way.
#
# Values are passed to psql as variables and quoted by psql itself
# (:"x" as an identifier, :'x' as a literal), so odd characters in a password
# cannot break or inject into the SQL.

set -euo pipefail

: "${APP_DB_USER:?APP_DB_USER must be set}"
: "${APP_DB_PASS:?APP_DB_PASS must be set}"
: "${APP_DB_NAME:?APP_DB_NAME must be set}"

psql -v ON_ERROR_STOP=1 \
     --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" \
     -v app_user="$APP_DB_USER" \
     -v app_pass="$APP_DB_PASS" \
     -v app_db="$APP_DB_NAME" <<'EOSQL'
CREATE ROLE :"app_user" WITH LOGIN PASSWORD :'app_pass';

SELECT format('CREATE DATABASE %I', :'app_db')
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = :'app_db')
\gexec

ALTER DATABASE :"app_db" OWNER TO :"app_user";
EOSQL
