#!/bin/bash

# ============================================================================
# Script para backup do banco de dados PostgreSQL
# ============================================================================

set -e

# Configurações
DB_NAME=${DB_NAME:-"move_marias"}
DB_USER=${DB_USER:-"postgres"}
BACKUP_DIR="./backups"
DATE=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="backup_${DB_NAME}_${DATE}.sql"

echo "🗄️ Iniciando backup do banco de dados..."

# Criar diretório de backup se não existir
mkdir -p "$BACKUP_DIR"

# Executar backup
echo "📦 Criando backup: $BACKUP_FILE"
docker-compose exec -T db pg_dump -U "$DB_USER" -d "$DB_NAME" --verbose --no-owner --no-acl > "$BACKUP_DIR/$BACKUP_FILE"

# Comprimir backup
echo "🗜️ Comprimindo backup..."
gzip "$BACKUP_DIR/$BACKUP_FILE"

echo "✅ Backup concluído: $BACKUP_DIR/$BACKUP_FILE.gz"

# Limpar backups antigos (manter apenas os últimos 7 dias)
echo "🧹 Limpando backups antigos..."
find "$BACKUP_DIR" -name "backup_*.sql.gz" -mtime +7 -delete

echo "🎉 Processo de backup finalizado!"
