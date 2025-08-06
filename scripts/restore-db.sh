#!/bin/bash

# ============================================================================
# Script para restaurar backup do banco de dados PostgreSQL
# ============================================================================

set -e

# Verificar se foi fornecido o arquivo de backup
if [ $# -eq 0 ]; then
    echo "❌ Uso: $0 <arquivo_backup.sql.gz>"
    echo "   Exemplo: $0 backups/backup_move_marias_20241201_120000.sql.gz"
    exit 1
fi

BACKUP_FILE="$1"
DB_NAME=${DB_NAME:-"move_marias"}
DB_USER=${DB_USER:-"postgres"}

# Verificar se o arquivo existe
if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ Arquivo de backup não encontrado: $BACKUP_FILE"
    exit 1
fi

echo "🔄 Iniciando restauração do banco de dados..."
echo "📁 Arquivo: $BACKUP_FILE"
echo "🗄️ Banco: $DB_NAME"

# Confirmar operação
read -p "⚠️  Esta operação irá SOBRESCREVER todos os dados existentes. Continuar? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Operação cancelada."
    exit 1
fi

# Parar aplicação
echo "🛑 Parando aplicação..."
docker-compose stop backend

# Descomprimir arquivo se necessário
if [[ "$BACKUP_FILE" == *.gz ]]; then
    echo "🗜️ Descomprimindo backup..."
    TEMP_FILE=$(mktemp)
    gunzip -c "$BACKUP_FILE" > "$TEMP_FILE"
    RESTORE_FILE="$TEMP_FILE"
else
    RESTORE_FILE="$BACKUP_FILE"
fi

# Dropar banco existente e recriar
echo "🗑️ Removendo banco existente..."
docker-compose exec db dropdb -U "$DB_USER" "$DB_NAME" || true
docker-compose exec db createdb -U "$DB_USER" "$DB_NAME"

# Restaurar backup
echo "📥 Restaurando backup..."
docker-compose exec -T db psql -U "$DB_USER" -d "$DB_NAME" < "$RESTORE_FILE"

# Limpar arquivo temporário
if [[ "$BACKUP_FILE" == *.gz ]]; then
    rm "$TEMP_FILE"
fi

# Reiniciar aplicação
echo "🚀 Reiniciando aplicação..."
docker-compose start backend

echo "✅ Restauração concluída com sucesso!"
echo "🎉 Banco de dados restaurado a partir de: $BACKUP_FILE"
