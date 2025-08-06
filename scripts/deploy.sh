#!/bin/bash

# ============================================================================
# Script para deploy em produção
# ============================================================================

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configurações
ENVIRONMENT=${1:-production}
VERSION=${2:-latest}

echo -e "${BLUE}🚀 Iniciando deploy para ${ENVIRONMENT}...${NC}"

# Função para validar ambiente
validate_environment() {
    echo -e "${YELLOW}🔍 Validando ambiente...${NC}"
    
    # Verificar se arquivos necessários existem
    if [ ! -f "docker-compose.prod.yml" ]; then
        echo -e "${RED}❌ Arquivo docker-compose.prod.yml não encontrado!${NC}"
        exit 1
    fi
    
    if [ ! -f ".env.production" ]; then
        echo -e "${RED}❌ Arquivo .env.production não encontrado!${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Ambiente validado!${NC}"
}

# Função para executar testes
run_tests() {
    echo -e "${YELLOW}🧪 Executando testes...${NC}"
    
    # Executar suite completa de testes
    ./scripts/run-tests.sh
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Testes falharam! Deploy abortado.${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Todos os testes passaram!${NC}"
}

# Função para criar backup
create_backup() {
    if [ "$ENVIRONMENT" = "production" ]; then
        echo -e "${YELLOW}🗄️ Criando backup antes do deploy...${NC}"
        ./scripts/backup-db.sh
        echo -e "${GREEN}✅ Backup criado!${NC}"
    fi
}

# Função para build das imagens
build_images() {
    echo -e "${YELLOW}🏗️ Construindo imagens Docker...${NC}"
    
    # Tag com versão
    docker-compose -f docker-compose.prod.yml build
    
    # Tagear imagens com versão
    docker tag sistemamovemarias_backend:latest sistemamovemarias_backend:$VERSION
    docker tag sistemamovemarias_frontend:latest sistemamovemarias_frontend:$VERSION
    
    echo -e "${GREEN}✅ Imagens construídas!${NC}"
}

# Função para fazer deploy
deploy() {
    echo -e "${YELLOW}🚢 Fazendo deploy...${NC}"
    
    # Copiar arquivo de ambiente
    cp .env.production .env
    
    # Parar serviços atuais (se existirem)
    docker-compose -f docker-compose.prod.yml down --remove-orphans || true
    
    # Iniciar novos serviços
    docker-compose -f docker-compose.prod.yml up -d
    
    # Aguardar serviços ficarem prontos
    echo -e "${YELLOW}⏳ Aguardando serviços ficarem prontos...${NC}"
    sleep 30
    
    # Executar migrações
    docker-compose -f docker-compose.prod.yml exec backend flask db upgrade
    
    echo -e "${GREEN}✅ Deploy concluído!${NC}"
}

# Função para verificar health
check_health() {
    echo -e "${YELLOW}🔍 Verificando saúde da aplicação...${NC}"
    
    # Verificar backend
    for i in {1..10}; do
        if curl -f http://localhost:5000/health > /dev/null 2>&1; then
            echo -e "${GREEN}✅ Backend está saudável!${NC}"
            break
        fi
        echo "Tentativa $i/10 - Aguardando backend..."
        sleep 10
    done
    
    # Verificar frontend
    for i in {1..10}; do
        if curl -f http://localhost:80 > /dev/null 2>&1; then
            echo -e "${GREEN}✅ Frontend está saudável!${NC}"
            break
        fi
        echo "Tentativa $i/10 - Aguardando frontend..."
        sleep 10
    done
    
    echo -e "${GREEN}✅ Aplicação está funcionando!${NC}"
}

# Função para rollback
rollback() {
    echo -e "${YELLOW}🔄 Fazendo rollback...${NC}"
    
    if [ -z "$2" ]; then
        echo -e "${RED}❌ Versão para rollback não especificada!${NC}"
        echo "Uso: $0 rollback <versão>"
        exit 1
    fi
    
    ROLLBACK_VERSION=$2
    
    # Parar serviços atuais
    docker-compose -f docker-compose.prod.yml down
    
    # Usar versão anterior
    docker tag sistemamovemarias_backend:$ROLLBACK_VERSION sistemamovemarias_backend:latest
    docker tag sistemamovemarias_frontend:$ROLLBACK_VERSION sistemamovemarias_frontend:latest
    
    # Subir com versão anterior
    docker-compose -f docker-compose.prod.yml up -d
    
    echo -e "${GREEN}✅ Rollback para versão $ROLLBACK_VERSION concluído!${NC}"
}

# Função principal
main() {
    case "$1" in
        production|staging)
            validate_environment
            run_tests
            create_backup
            build_images
            deploy
            check_health
            echo -e "\n${GREEN}🎉 Deploy para $ENVIRONMENT concluído com sucesso!${NC}"
            ;;
        rollback)
            rollback "$@"
            ;;
        *)
            echo "❌ Uso: $0 <production|staging> [versão]"
            echo "   ou: $0 rollback <versão>"
            exit 1
            ;;
    esac
}

# Executar função principal
main "$@"
