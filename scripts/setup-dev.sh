#!/bin/bash

# ============================================================================
# Script para inicializar o ambiente de desenvolvimento
# ============================================================================

set -e  # Parar em caso de erro

echo "🚀 Inicializando ambiente de desenvolvimento Move Marias..."

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não encontrado. Por favor, instale o Docker primeiro."
    exit 1
fi

# Verificar se Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose não encontrado. Por favor, instale o Docker Compose primeiro."
    exit 1
fi

# Criar arquivo .env se não existir
if [ ! -f .env ]; then
    echo "📝 Criando arquivo .env..."
    cp .env.example .env
    echo "✅ Arquivo .env criado. Edite-o conforme necessário."
fi

# Criar arquivo .env do frontend se não existir
if [ ! -f frontend/.env ]; then
    echo "📝 Criando arquivo .env do frontend..."
    cp frontend/.env.example frontend/.env
    echo "✅ Arquivo .env do frontend criado."
fi

# Criar diretórios necessários
echo "📁 Criando diretórios necessários..."
mkdir -p logs backups uploads

# Definir permissões
chmod 755 logs backups uploads

echo "🐳 Construindo containers Docker..."
docker-compose build

echo "🗄️ Iniciando banco de dados..."
docker-compose up -d db

echo "⏳ Aguardando banco de dados ficar pronto..."
sleep 10

echo "🔧 Inicializando banco de dados..."
docker-compose run --rm backend python seed_data.py

echo "🌟 Iniciando todos os serviços..."
docker-compose up -d

echo ""
echo "✅ Ambiente de desenvolvimento inicializado com sucesso!"
echo ""
echo "🔗 URLs disponíveis:"
echo "   - Frontend: http://localhost:3000"
echo "   - Backend API: http://localhost:5000"
echo "   - pgAdmin: http://localhost:8080"
echo ""
echo "👤 Usuários padrão:"
echo "   - Admin: admin@movemarias.dev / admin123"
echo "   - Profissional: profissional@movemarias.dev / prof123"
echo ""
echo "📋 Comandos úteis:"
echo "   - Ver logs: docker-compose logs -f"
echo "   - Parar serviços: docker-compose down"
echo "   - Resetar banco: docker-compose run --rm backend flask reset-db"
echo ""
echo "🎉 Bom desenvolvimento!"
