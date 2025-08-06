# ============================================================================
# Multi-stage Dockerfile para Frontend React
# ============================================================================

# Imagem base com Node.js
FROM node:18-alpine as base

# Definir variáveis de ambiente
ENV NODE_ENV=development
ENV CHOKIDAR_USEPOLLING=true
ENV WATCHPACK_POLLING=true

# Instalar dependências do sistema
RUN apk add --no-cache \
    git \
    python3 \
    make \
    g++

# Criar usuário não-root para segurança
RUN addgroup -g 1001 -S nodejs && \
    adduser -S reactjs -u 1001

# Criar diretório da aplicação
WORKDIR /app

# Alterar ownership do diretório
RUN chown -R reactjs:nodejs /app

# ============================================================================
# Stage de desenvolvimento
# ============================================================================
FROM base as development

# Copiar package.json e package-lock.json primeiro para aproveitar cache
COPY package*.json ./

# Instalar dependências
RUN npm ci --only=development

# Copiar código da aplicação
COPY . .

# Mudar ownership para o usuário da aplicação
RUN chown -R reactjs:nodejs /app

# Usar usuário não-root
USER reactjs

# Expor porta da aplicação
EXPOSE 3000

# Comando padrão para desenvolvimento
CMD ["npm", "start"]

# ============================================================================
# Stage de build para produção
# ============================================================================
FROM base as build

# Copiar package.json e package-lock.json
COPY package*.json ./

# Instalar dependências
RUN npm ci --only=production

# Copiar código da aplicação
COPY . .

# Build da aplicação
RUN npm run build

# ============================================================================
# Stage de produção com Nginx
# ============================================================================
FROM nginx:alpine as production

# Copiar arquivos build
COPY --from=build /app/build /usr/share/nginx/html

# Copiar configuração customizada do Nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Expor porta 80
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:80/ || exit 1

# Comando padrão
CMD ["nginx", "-g", "daemon off;"]
