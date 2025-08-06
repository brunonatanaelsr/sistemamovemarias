#!/bin/bash

# ============================================================================
# Script para monitorar logs da aplicação
# ============================================================================

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para mostrar ajuda
show_help() {
    echo "🔍 Monitor de Logs - Sistema Move Marias"
    echo ""
    echo "Uso: $0 [OPÇÕES] [SERVIÇO]"
    echo ""
    echo "SERVIÇOS:"
    echo "  all        - Todos os serviços (padrão)"
    echo "  backend    - API Backend"
    echo "  frontend   - Interface Frontend"
    echo "  db         - Banco de dados PostgreSQL"
    echo "  nginx      - Servidor web"
    echo ""
    echo "OPÇÕES:"
    echo "  -f, --follow     - Seguir logs em tempo real"
    echo "  -n, --lines N    - Mostrar últimas N linhas (padrão: 100)"
    echo "  -t, --tail       - Mostrar apenas logs novos"
    echo "  -e, --errors     - Filtrar apenas erros"
    echo "  -h, --help       - Mostrar esta ajuda"
    echo ""
    echo "EXEMPLOS:"
    echo "  $0 backend -f           # Seguir logs do backend"
    echo "  $0 -n 50 frontend       # Últimas 50 linhas do frontend"
    echo "  $0 --errors             # Apenas erros de todos os serviços"
}

# Variáveis padrão
SERVICE="all"
FOLLOW=false
LINES=100
TAIL_ONLY=false
ERRORS_ONLY=false

# Processar argumentos
while [[ $# -gt 0 ]]; do
    case $1 in
        -f|--follow)
            FOLLOW=true
            shift
            ;;
        -n|--lines)
            LINES="$2"
            shift 2
            ;;
        -t|--tail)
            TAIL_ONLY=true
            shift
            ;;
        -e|--errors)
            ERRORS_ONLY=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        backend|frontend|db|nginx|all)
            SERVICE="$1"
            shift
            ;;
        *)
            echo -e "${RED}❌ Opção desconhecida: $1${NC}"
            show_help
            exit 1
            ;;
    esac
done

# Função para construir comando docker-compose logs
build_log_command() {
    local cmd="docker-compose logs"
    
    if [ "$FOLLOW" = true ]; then
        cmd="$cmd -f"
    fi
    
    if [ "$TAIL_ONLY" = true ]; then
        cmd="$cmd --tail=0"
    else
        cmd="$cmd --tail=$LINES"
    fi
    
    # Adicionar serviço se não for 'all'
    if [ "$SERVICE" != "all" ]; then
        cmd="$cmd $SERVICE"
    fi
    
    echo "$cmd"
}

# Função para filtrar erros
filter_errors() {
    if [ "$ERRORS_ONLY" = true ]; then
        grep -i "error\|exception\|fail\|critical\|fatal" || true
    else
        cat
    fi
}

# Função principal
main() {
    echo -e "${BLUE}🔍 Monitorando logs do Sistema Move Marias${NC}"
    echo -e "${YELLOW}Serviço: $SERVICE${NC}"
    
    if [ "$FOLLOW" = true ]; then
        echo -e "${GREEN}📡 Modo: Tempo real${NC}"
    else
        echo -e "${GREEN}📋 Modo: Últimas $LINES linhas${NC}"
    fi
    
    if [ "$ERRORS_ONLY" = true ]; then
        echo -e "${RED}🔥 Filtro: Apenas erros${NC}"
    fi
    
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    # Verificar se os containers estão rodando
    if ! docker-compose ps | grep -q "Up"; then
        echo -e "${RED}❌ Nenhum container está rodando!${NC}"
        echo "Execute: docker-compose up -d"
        exit 1
    fi
    
    # Construir e executar comando
    cmd=$(build_log_command)
    echo -e "${BLUE}Executando: $cmd${NC}"
    echo ""
    
    eval "$cmd" | filter_errors
}

# Executar função principal
main
