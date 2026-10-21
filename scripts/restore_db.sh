#!/usr/bin/env bash
# Database Restoration Script for Circular Economy Platform
set -euo pipefail

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 /path/to/backup_file.sql.gz"
    exit 1
fi

BACKUP_FILE="$1"
CONTAINER_NAME="circular_economy_postgres"
DB_NAME="circular_economy"
DB_USER="postgres"

if [ ! -f "${BACKUP_FILE}" ]; then
    echo "[ERROR] Backup file not found: ${BACKUP_FILE}"
    exit 1
fi

echo "[WARNING] Restoring database will overwrite existing data in '${DB_NAME}'."
read -p "Are you sure you want to proceed? (y/N): " confirm
if [[ "${confirm}" != "y" && "${confirm}" != "Y" ]]; then
    echo "Restoration cancelled."
    exit 0
fi

echo "[INFO] Restoring database from ${BACKUP_FILE}..."

# Drop connections, drop/recreate database and restore from compressed SQL dump
gunzip -c "${BACKUP_FILE}" | docker exec -i "${CONTAINER_NAME}" psql -U "${DB_USER}" -d "${DB_NAME}"

echo "[SUCCESS] Database restored successfully from ${BACKUP_FILE}."
