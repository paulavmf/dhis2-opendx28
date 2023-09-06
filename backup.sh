#!/bin/bash


CONTAINER_NAME="dhis2-opendx28-db-1"
DATABASE_NAME="dhis"
OUTPUT_FOLDER="/home/paula/Documentos/opendx28/dhis2-opendx28"
OUTPUT_FILE="dump.sql.gz"
PG_USER="dhis"
PG_PASSWORD="dhis"

# Backup and compress
docker exec $CONTAINER_NAME pg_dump -U $PG_USER -d $DATABASE_NAME | gzip > $OUTPUT_FOLDER/$OUTPUT_FILE

echo "Backup completed and saved to $OUTPUT_FOLDER/$OUTPUT_FILE"
