#!/bin/bash

# ============================================================================
# Script para limpar ambiente de desenvolvimento
# ============================================================================

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🧹 Limpeza do Ambiente de Desenvolvimento${NC}"

# Função para confirmar ação
confirm_action() {
    local message="$1"
    echo -e "${YELLOW}⚠️  $message${NC}"
    read -p "Continuar? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${RED}❌ Operação cancelada.${NC}"
        exit 1
    fi
}

# Função para parar e remover containers
stop_containers() {
    echo -e "\n${YELLOW}🛑 Parando containers...${NC}"
    docker-compose down --remove-orphans
    echo -e "${GREEN}✅ Containers parados!${NC}"
}

# Função para remover volumes
remove_volumes() {
    echo -e "\n${YELLOW}🗑️ Removendo volumes...${NC}"
    docker-compose down -v
    docker volume prune -f
    echo -e "${GREEN}✅ Volumes removidos!${NC}"
}

# Função para remover imagens
remove_images() {
    echo -e "\n${YELLOW}🖼️ Removendo imagens...${NC}"
    
    # Remover imagens do projeto
    docker images | grep sistemamovemarias | awk '{print $3}' | xargs -r docker rmi -f
    
    # Remover imagens órfãs
    docker image prune -f
    
    echo -e "${GREEN}✅ Imagens removidas!${NC}"
}

# Função para limpar cache do Docker
clean_docker_cache() {
    echo -e "\n${YELLOW}🗂️ Limpando cache do Docker...${NC}"
    docker system prune -f --volumes
    echo -e "${GREEN}✅ Cache limpo!${NC}"
}

# Função para limpar logs
clean_logs() {
    echo -e "\n${YELLOW}📝 Limpando logs...${NC}"
    if [ -d "logs" ]; then
        rm -rf logs/*
        echo -e "${GREEN}✅ Logs limpos!${NC}"
    else
        echo -e "${BLUE}ℹ️ Diretório de logs não encontrado.${NC}"
    fi
}

# Função para limpar backups antigos
clean_old_backups() {
    echo -e "\n${YELLOW}🗄️ Limpando backups antigos (>30 dias)...${NC}"
    if [ -d "backups" ]; then
        find backups/ -name "*.sql.gz" -mtime +30 -delete
        echo -e "${GREEN}✅ Backups antigos removidos!${NC}"
    else
        echo -e "${BLUE}ℹ️ Diretório de backups não encontrado.${NC}"
    fi
}

# Função para limpar dependências do frontend
clean_frontend_deps() {
    echo -e "\n${YELLOW}📦 Limpando dependências do frontend...${NC}"
    if [ -d "frontend/node_modules" ]; then
        rm -rf frontend/node_modules
        echo -e "${GREEN}✅ node_modules removido!${NC}"
    fi
    
    if [ -f "frontend/package-lock.json" ]; then
        rm frontend/package-lock.json
        echo -e "${GREEN}✅ package-lock.json removido!${NC}"
    fi
}

# Função para limpar cache do Python
clean_python_cache() {
    echo -e "\n${YELLOW}🐍 Limpando cache do Python...${NC}"
    find backend/ -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find backend/ -name "*.pyc" -delete 2>/dev/null || true
    echo -e "${GREEN}✅ Cache do Python limpo!${NC}"
}

# Função para limpeza completa
full_cleanup() {
    confirm_action "Esta operação irá remover TODOS os dados, incluindo banco de dados e volumes. Esta ação é IRREVERSÍVEL!"
    
    stop_containers
    remove_volumes
    remove_images
    clean_docker_cache
    clean_logs
    clean_old_backups
    clean_frontend_deps
    clean_python_cache
    
    echo -e "\n${GREEN}🎉 Limpeza completa finalizada!${NC}"
    echo -e "${BLUE}Para reinicializar o ambiente, execute: ./scripts/setup-dev.sh${NC}"
}

# Função para limpeza básica
basic_cleanup() {
    stop_containers
    clean_logs
    clean_python_cache
    
    echo -e "\n${GREEN}🎉 Limpeza básica finalizada!${NC}"
}

# Função para limpeza de desenvolvimento
dev_cleanup() {
    stop_containers
    clean_frontend_deps
    clean_python_cache
    clean_logs
    
    echo -e "\n${GREEN}🎉 Limpeza de desenvolvimento finalizada!${NC}"
}

# Função para mostrar ajuda
show_help() {
    echo "🧹 Script de Limpeza - Sistema Move Marias"
    echo ""
    echo "Uso: $0 [OPÇÃO]"
    echo ""
    echo "OPÇÕES:"
    echo "  full     - Limpeza completa (remove tudo, incluindo dados)"
    echo "  basic    - Limpeza básica (para containers e logs)"
    echo "  dev      - Limpeza de desenvolvimento (deps e cache)"
    echo "  help     - Mostrar esta ajuda"
    echo ""
    echo "CUIDADO:"
    echo "  A opção 'full' remove TODOS os dados permanentemente!"
}

# Função principal
main() {
    case "${1:-basic}" in
        full)
            full_cleanup
            ;;
        basic)
            basic_cleanup
            ;;
        dev)
            dev_cleanup
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            echo -e "${RED}❌ Opção inválida: $1${NC}"
            show_help
            exit 1
            ;;
    esac
}

# Executar função principal
main "$@"
