#!/bin/bash

# ============================================================================
# Script para executar testes automatizados
# ============================================================================

set -e

echo "🧪 Executando testes do Sistema Move Marias..."

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para executar testes do backend
run_backend_tests() {
    echo -e "\n${YELLOW}🐍 Executando testes do Backend...${NC}"
    
    # Verificar se o container do backend está rodando
    if ! docker-compose ps backend | grep -q "Up"; then
        echo "🚀 Iniciando container do backend..."
        docker-compose up -d backend
        sleep 5
    fi
    
    # Executar testes
    docker-compose exec backend python -m pytest tests/ -v --tb=short --cov=app --cov-report=term-missing
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Testes do backend passaram!${NC}"
    else
        echo -e "${RED}❌ Testes do backend falharam!${NC}"
        return 1
    fi
}

# Função para executar testes do frontend
run_frontend_tests() {
    echo -e "\n${YELLOW}⚛️ Executando testes do Frontend...${NC}"
    
    # Verificar se o container do frontend está rodando
    if ! docker-compose ps frontend | grep -q "Up"; then
        echo "🚀 Iniciando container do frontend..."
        docker-compose up -d frontend
        sleep 10
    fi
    
    # Executar testes
    docker-compose exec frontend npm test -- --coverage --watchAll=false
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Testes do frontend passaram!${NC}"
    else
        echo -e "${RED}❌ Testes do frontend falharam!${NC}"
        return 1
    fi
}

# Função para executar linting
run_linting() {
    echo -e "\n${YELLOW}🔍 Executando análise de código...${NC}"
    
    # Backend linting
    echo "🐍 Verificando código Python..."
    docker-compose exec backend flake8 app/ --max-line-length=88 --exclude=migrations
    docker-compose exec backend black --check app/
    
    # Frontend linting
    echo "⚛️ Verificando código JavaScript/React..."
    docker-compose exec frontend npm run lint
    
    echo -e "${GREEN}✅ Análise de código concluída!${NC}"
}

# Função para executar testes de integração
run_integration_tests() {
    echo -e "\n${YELLOW}🔗 Executando testes de integração...${NC}"
    
    # Aguardar todos os serviços estarem prontos
    echo "⏳ Aguardando serviços ficarem prontos..."
    sleep 15
    
    # Executar testes de integração
    docker-compose exec backend python -m pytest tests/integration/ -v
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Testes de integração passaram!${NC}"
    else
        echo -e "${RED}❌ Testes de integração falharam!${NC}"
        return 1
    fi
}

# Função principal
main() {
    # Verificar argumentos
    if [ $# -eq 0 ]; then
        echo "Executando todos os testes..."
        run_backend_tests
        run_frontend_tests
        run_linting
        run_integration_tests
    else
        case "$1" in
            backend)
                run_backend_tests
                ;;
            frontend)
                run_frontend_tests
                ;;
            lint)
                run_linting
                ;;
            integration)
                run_integration_tests
                ;;
            *)
                echo "❌ Uso: $0 [backend|frontend|lint|integration]"
                echo "   Sem argumentos: executa todos os testes"
                exit 1
                ;;
        esac
    fi
    
    echo -e "\n${GREEN}🎉 Testes concluídos!${NC}"
}

# Executar função principal
main "$@"
