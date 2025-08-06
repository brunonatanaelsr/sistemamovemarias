# Sistema Move Marias - Scripts de Desenvolvimento

Este diretório contém scripts utilitários para facilitar o desenvolvimento e manutenção do Sistema Move Marias.

## 📋 Scripts Disponíveis

### 🚀 `setup-dev.sh`
**Inicialização do ambiente de desenvolvimento**

Configura completamente o ambiente de desenvolvimento, incluindo:
- Verificação de dependências (Docker, Docker Compose)
- Criação de arquivos `.env` necessários
- Construção e inicialização dos containers
- Inicialização do banco de dados
- População com dados iniciais

```bash
./scripts/setup-dev.sh
```

**URLs após a execução:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- pgAdmin: http://localhost:8080

**Usuários padrão:**
- Admin: `admin@movemarias.dev` / `admin123`
- Profissional: `profissional@movemarias.dev` / `prof123`

### 🗄️ `backup-db.sh`
**Backup do banco de dados**

Cria backup comprimido do banco PostgreSQL com timestamp:

```bash
./scripts/backup-db.sh
```

- Salva em `./backups/backup_move_marias_YYYYMMDD_HHMMSS.sql.gz`
- Remove automaticamente backups com mais de 7 dias
- Utiliza `pg_dump` via container Docker

### 🔄 `restore-db.sh`
**Restauração do banco de dados**

Restaura banco a partir de arquivo de backup:

```bash
./scripts/restore-db.sh backups/backup_move_marias_20241201_120000.sql.gz
```

**⚠️ ATENÇÃO:** Esta operação **sobrescreve** todos os dados existentes!

### 🧪 `run-tests.sh`
**Execução de testes automatizados**

Executa suite completa de testes ou testes específicos:

```bash
# Todos os testes
./scripts/run-tests.sh

# Testes específicos
./scripts/run-tests.sh backend     # Backend apenas
./scripts/run-tests.sh frontend    # Frontend apenas
./scripts/run-tests.sh lint        # Análise de código
./scripts/run-tests.sh integration # Testes de integração
```

**Inclui:**
- Testes unitários (pytest para backend, Jest para frontend)
- Análise de código (flake8, black, ESLint)
- Testes de integração
- Relatórios de cobertura

### 🚢 `deploy.sh`
**Deploy para produção**

Automatiza o processo completo de deploy:

```bash
# Deploy para produção
./scripts/deploy.sh production v1.0.0

# Deploy para staging
./scripts/deploy.sh staging

# Rollback
./scripts/deploy.sh rollback v0.9.0
```

**Processo inclui:**
- Validação do ambiente
- Execução de testes
- Backup automático (produção)
- Build das imagens Docker
- Deploy com verificação de saúde
- Rollback automático em caso de falha

### 🔍 `monitor-logs.sh`
**Monitoramento de logs**

Facilita visualização e monitoramento dos logs:

```bash
# Todos os logs em tempo real
./scripts/monitor-logs.sh -f

# Backend apenas
./scripts/monitor-logs.sh backend -f

# Últimas 50 linhas do frontend
./scripts/monitor-logs.sh -n 50 frontend

# Apenas erros
./scripts/monitor-logs.sh --errors
```

**Opções:**
- `-f, --follow`: Tempo real
- `-n, --lines N`: Número de linhas
- `-e, --errors`: Filtrar apenas erros
- Suporte a cores para melhor visualização

### 🧹 `cleanup.sh`
**Limpeza do ambiente**

Remove dados temporários e reseta o ambiente:

```bash
# Limpeza básica (containers e logs)
./scripts/cleanup.sh basic

# Limpeza de desenvolvimento (deps e cache)
./scripts/cleanup.sh dev

# Limpeza completa (REMOVE TODOS OS DADOS!)
./scripts/cleanup.sh full
```

**Tipos de limpeza:**
- **Basic**: Para containers, limpa logs
- **Dev**: Remove dependências e cache
- **Full**: ⚠️ Remove TUDO (dados, volumes, imagens)

## 🛠️ Uso Geral

### Fluxo de Desenvolvimento Típico

1. **Configuração inicial:**
   ```bash
   ./scripts/setup-dev.sh
   ```

2. **Durante desenvolvimento:**
   ```bash
   # Monitorar logs
   ./scripts/monitor-logs.sh backend -f
   
   # Executar testes
   ./scripts/run-tests.sh
   ```

3. **Backup periódico:**
   ```bash
   ./scripts/backup-db.sh
   ```

4. **Limpeza quando necessário:**
   ```bash
   ./scripts/cleanup.sh dev
   ```

### Deploy para Produção

```bash
# 1. Executar testes
./scripts/run-tests.sh

# 2. Fazer deploy
./scripts/deploy.sh production v1.0.0

# 3. Monitorar aplicação
./scripts/monitor-logs.sh -f
```

## 📁 Estrutura de Arquivos Gerados

```
/workspaces/sistemamovemarias/
├── logs/           # Logs da aplicação
├── backups/        # Backups do banco de dados
├── uploads/        # Arquivos enviados pelos usuários
├── .env           # Configurações de ambiente
└── frontend/.env  # Configurações do frontend
```

## 🔧 Configuração

### Variáveis de Ambiente

Os scripts utilizam as seguintes variáveis (definidas nos arquivos `.env`):

- `DB_NAME`: Nome do banco de dados
- `DB_USER`: Usuário do PostgreSQL
- `DEFAULT_ADMIN_EMAIL`: Email do administrador padrão
- `DEFAULT_ADMIN_PASSWORD`: Senha do administrador padrão

### Dependências

- Docker 20.10+
- Docker Compose 2.0+
- Bash 4.0+
- curl (para health checks)

## 🐛 Solução de Problemas

### Container não inicia
```bash
./scripts/cleanup.sh basic
./scripts/setup-dev.sh
```

### Erro de permissão
```bash
chmod +x scripts/*.sh
```

### Banco de dados corrompido
```bash
./scripts/restore-db.sh backups/backup_mais_recente.sql.gz
```

### Performance lenta
```bash
./scripts/cleanup.sh dev
docker system prune -f
```

## 📞 Suporte

Para problemas com os scripts:
1. Verificar logs: `./scripts/monitor-logs.sh --errors`
2. Verificar status: `docker-compose ps`
3. Limpar ambiente: `./scripts/cleanup.sh basic`
4. Reinicializar: `./scripts/setup-dev.sh`
