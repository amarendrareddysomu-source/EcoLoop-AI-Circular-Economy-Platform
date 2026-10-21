#!/usr/bin/env bash
# Automated PostgreSQL Database Backup Script for Circular Economy Platform
set -euo pipefail

BACKUP_DIR="${BACKUP_DIR:-/var/backups/circular_economy}"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
CONTAINER_NAME="circular_economy_postgres"
DB_NAME="circular_economy"
DB_USER="postgres"
BACKUP_FILE="${BACKUP_DIR}/db_backup_${TIMESTAMP}.sql.gz"

mkdir -p "${BACKUP_DIR}"

echo "[INFO] Starting database backup for '${DB_NAME}' at ${TIMESTAMP}..."

# Execute pg_dump inside container and compress output
docker exec -t "${CONTAINER_NAME}" pg_dump -U "${DB_USER}" "${DB_NAME}" | gzip > "${BACKUP_FILE}"

echo "[SUCCESS] Database backup saved to: ${BACKUP_FILE}"
echo "[INFO] Size: $(du -h "${BACKUP_FILE}" | cut -f1)"

# Rotation: Purge backups older than 30 days
find "${BACKUP_DIR}" -type f -name "db_backup_*.sql.gz" -mtime +30 -delete
echo "[INFO] Rotated backups older than 30 days."
