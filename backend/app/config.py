"""
Configurações da aplicação Flask.

Este módulo contém todas as configurações de ambiente para o
Sistema Move Marias.
"""

import os
from datetime import timedelta


class Config:
    """Configurações base da aplicação."""
    
    # Configurações básicas do Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Configurações do banco de dados
    DATABASE_URL = os.environ.get('DATABASE_URL') or 
        'postgresql://postgres:postgres@localhost:5432/move_marias'
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_timeout': 20,
        'pool_recycle': -1,
        'pool_pre_ping': True
    }
    
    # Configurações do Redis
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    
    # Configurações JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_ALGORITHM = 'HS256'
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    
    # Configurações de CORS
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    # Configurações de upload
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # Configurações de logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    LOG_FILE = os.environ.get('LOG_FILE') or 'logs/app.log'
    
    # Configurações de email (para futuras funcionalidades)
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # Configurações da aplicação
    APP_NAME = 'Sistema Move Marias'
    APP_VERSION = '1.0.0'
    
    # Configurações de paginação
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100
    
    # Configurações de segurança
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Usuários padrão (para seeding)
    DEFAULT_ADMIN_EMAIL = os.environ.get('DEFAULT_ADMIN_EMAIL') or 'admin@movemarias.dev'
    DEFAULT_ADMIN_PASSWORD = os.environ.get('DEFAULT_ADMIN_PASSWORD') or 'admin123'
    DEFAULT_PROF_EMAIL = os.environ.get('DEFAULT_PROF_EMAIL') or 'profissional@movemarias.dev'
    DEFAULT_PROF_PASSWORD = os.environ.get('DEFAULT_PROF_PASSWORD') or 'prof123'
    
    # Configurações para seeding
    SEED_DATABASE = os.environ.get('SEED_DATABASE', 'true').lower() in ['true', 'on', '1']


class DevelopmentConfig(Config):
    """Configurações para ambiente de desenvolvimento."""
    
    DEBUG = True
    TESTING = False
    
    # Configurações menos restritivas para desenvolvimento
    SESSION_COOKIE_SECURE = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=8)
    
    # Logging mais verboso
    LOG_LEVEL = 'DEBUG'
    
    # CORS mais permissivo
    CORS_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000']


class TestingConfig(Config):
    """Configurações para ambiente de testes."""
    
    TESTING = True
    DEBUG = True
    
    # Banco de dados em memória para testes
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # JWT com expiração curta para testes
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=1)
    
    # Desabilitar CSRF para testes
    WTF_CSRF_ENABLED = False
    
    # Não fazer seeding em testes
    SEED_DATABASE = False


class ProductionConfig(Config):
    """Configurações para ambiente de produção."""
    
    DEBUG = False
    TESTING = False
    
    # Configurações mais restritivas para produção
    SESSION_COOKIE_SECURE = True
    
    # Logging menos verboso
    LOG_LEVEL = 'WARNING'
    
    # CORS restritivo
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '').split(',')
    
    # Não fazer seeding em produção
    SEED_DATABASE = False
    
    # Configurações de segurança adicional
    PREFERRED_URL_SCHEME = 'https'


class StagingConfig(ProductionConfig):
    """Configurações para ambiente de staging."""
    
    DEBUG = True
    LOG_LEVEL = 'INFO'
    
    # Permitir seeding em staging
    SEED_DATABASE = True


# Mapeamento de configurações por ambiente
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig
}


def get_config():
    """
    Obter configuração baseada na variável de ambiente.
    
    Returns:
        Config: Classe de configuração apropriada
    """
    env = os.environ.get('FLASK_ENV') or 'development'
    return config_by_name.get(env, DevelopmentConfig)nfigurações da aplicação Flask.

Este módulo contém as classes de configuração para diferentes ambientes
(development, testing, production).
"""

import os
from datetime import timedelta


class Config:
    """Configuração base para todos os ambientes."""
    
    # Configurações básicas do Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Configurações do banco de dados
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://movemarias_user:movemarias_password@localhost:5432/movemarias_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True
    }
    
    # Configurações JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 1440)))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 30)))
    JWT_ALGORITHM = 'HS256'
    
    # Configurações de CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
    
    # Configurações de upload
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads/')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16)) * 1024 * 1024  # MB
    ALLOWED_EXTENSIONS = set(os.getenv('ALLOWED_EXTENSIONS', 'pdf,doc,docx,jpg,jpeg,png').split(','))
    
    # Configurações de email
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@movemarias.org')
    
    # Configurações de cache
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Configurações de segurança
    RATE_LIMIT = int(os.getenv('RATE_LIMIT', 100))
    LOGIN_ATTEMPT_TIMEOUT = int(os.getenv('LOGIN_ATTEMPT_TIMEOUT', 15))
    MAX_LOGIN_ATTEMPTS = int(os.getenv('MAX_LOGIN_ATTEMPTS', 5))
    
    # Configurações de logs
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')
    
    # Configurações LGPD
    DATA_RETENTION_YEARS = int(os.getenv('DATA_RETENTION_YEARS', 5))
    DPO_EMAIL = os.getenv('DPO_EMAIL', 'dpo@movemarias.org')
    
    # Configurações de backup
    BACKUP_DIR = os.getenv('BACKUP_DIR', 'backups/')
    BACKUP_RETENTION_DAYS = int(os.getenv('BACKUP_RETENTION_DAYS', 30))
    
    # Configurações de monitoramento
    SENTRY_DSN = os.getenv('SENTRY_DSN')
    
    # Timezone
    TIMEZONE = 'America/Sao_Paulo'


class DevelopmentConfig(Config):
    """Configuração para ambiente de desenvolvimento."""
    
    DEBUG = True
    TESTING = False
    
    # Logs mais verbosos em desenvolvimento
    LOG_LEVEL = 'DEBUG'
    
    # Cache desabilitado para desenvolvimento
    CACHE_TYPE = 'null'
    
    # Rate limiting mais permissivo
    RATE_LIMIT = 1000
    
    # Seed database
    SEED_DATABASE = os.getenv('SEED_DATABASE', 'True').lower() == 'true'
    
    # Usuários padrão para desenvolvimento
    DEFAULT_ADMIN_EMAIL = os.getenv('DEFAULT_ADMIN_EMAIL', 'admin@movemarias.dev')
    DEFAULT_ADMIN_PASSWORD = os.getenv('DEFAULT_ADMIN_PASSWORD', 'admin123')
    DEFAULT_PROF_EMAIL = os.getenv('DEFAULT_PROF_EMAIL', 'profissional@movemarias.dev')
    DEFAULT_PROF_PASSWORD = os.getenv('DEFAULT_PROF_PASSWORD', 'prof123')


class TestingConfig(Config):
    """Configuração para ambiente de testes."""
    
    TESTING = True
    DEBUG = False
    
    # Banco de dados em memória para testes
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # JWT com expiração mais curta para testes
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=10)
    
    # Cache desabilitado para testes
    CACHE_TYPE = 'null'
    
    # Rate limiting desabilitado para testes
    RATELIMIT_ENABLED = False
    
    # Desabilitar logs durante testes
    LOG_LEVEL = 'ERROR'
    
    # CSRF desabilitado para testes
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Configuração para ambiente de produção."""
    
    DEBUG = False
    TESTING = False
    
    # Configurações de segurança mais restritivas
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # SSL Configuration
    SSL_CERTIFICATE_PATH = os.getenv('SSL_CERTIFICATE_PATH')
    SSL_PRIVATE_KEY_PATH = os.getenv('SSL_PRIVATE_KEY_PATH')
    
    # Domain configuration
    SERVER_NAME = os.getenv('DOMAIN_NAME')
    
    # Logs mais restritivos em produção
    LOG_LEVEL = 'WARNING'
    
    # Rate limiting mais restritivo
    RATE_LIMIT = 60


class StagingConfig(ProductionConfig):
    """Configuração para ambiente de staging."""
    
    DEBUG = True
    
    # Logs mais verbosos em staging
    LOG_LEVEL = 'INFO'
    
    # Rate limiting mais permissivo que produção
    RATE_LIMIT = 100


# Mapeamento de configurações
config_map = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'staging': StagingConfig,
    'default': DevelopmentConfig
}


def get_config(config_name=None):
    """
    Retorna a classe de configuração apropriada.
    
    Args:
        config_name (str): Nome da configuração ('development', 'testing', 'production', 'staging')
    
    Returns:
        Config: Classe de configuração
    """
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    return config_map.get(config_name, DevelopmentConfig)
