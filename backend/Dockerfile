# ============================================================================
# Multi-stage Dockerfile para Backend Flask
# ============================================================================

# Imagem base com Python 3.11 slim
FROM python:3.11-slim as base

# Definir variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Criar usuário não-root para segurança
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Criar diretórios da aplicação
RUN mkdir -p /app/uploads /app/logs /app/temp && \
    chown -R appuser:appuser /app

# Definir diretório de trabalho
WORKDIR /app

# ============================================================================
# Stage de desenvolvimento
# ============================================================================
FROM base as development

# Instalar dependências de desenvolvimento
RUN apt-get update && apt-get install -y \
    git \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primeiro para aproveitar cache do Docker
COPY requirements.txt requirements-dev.txt ./

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements-dev.txt

# Copiar código da aplicação
COPY . .

# Mudar ownership para o usuário da aplicação
RUN chown -R appuser:appuser /app

# Usar usuário não-root
USER appuser

# Expor porta da aplicação
EXPOSE 5000

# Comando padrão para desenvolvimento
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000", "--debug"]

# ============================================================================
# Stage de produção
# ============================================================================
FROM base as production

# Copiar requirements
COPY requirements.txt ./

# Instalar apenas dependências de produção
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Mudar ownership para o usuário da aplicação
RUN chown -R appuser:appuser /app

# Usar usuário não-root
USER appuser

# Expor porta da aplicação
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/api/health || exit 1

# Comando padrão para produção
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "app:create_app()"]

# ============================================================================
# Stage de testes
# ============================================================================
FROM development as testing

# Instalar dependências adicionais para testes
RUN pip install --no-cache-dir pytest-cov pytest-mock coverage

# Executar testes
CMD ["python", "-m", "pytest", "--cov=.", "--cov-report=html", "--cov-report=term"]
