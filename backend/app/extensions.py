"""
Inicialização de extensões Flask.

Este módulo centraliza a inicialização de todas as extensões
utilizadas na aplicação.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from flask_redis import FlaskRedis
from flask_bcrypt import Bcrypt
from flask_caching import Cache
import logging
from logging.handlers import RotatingFileHandler
import os

# Inicialização das extensões
db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()
cors = CORS()
migrate = Migrate()
redis_client = FlaskRedis()
bcrypt = Bcrypt()
cache = Cache()


def init_extensions(app):
    """
    Inicializar todas as extensões com a aplicação Flask.
    
    Args:
        app: Instância da aplicação Flask
    """
    # Banco de dados
    db.init_app(app)
    
    # Serialização
    ma.init_app(app)
    
    # Criptografia
    bcrypt.init_app(app)
    
    # Cache
    cache.init_app(app)
    
    # JWT
    jwt.init_app(app)
    
    # CORS
    cors.init_app(app, origins=app.config.get('CORS_ORIGINS', ['*']))
    
    # Migrações
    migrate.init_app(app, db)
    
    # Redis (se configurado)
    if app.config.get('REDIS_URL'):
        redis_client.init_app(app)
    
    # Configurar logging
    setup_logging(app)
    
    # Configurar handlers JWT
    setup_jwt_handlers(app)


def setup_logging(app):
    """
    Configurar sistema de logging da aplicação.
    
    Args:
        app: Instância da aplicação Flask
    """
    if not app.debug and not app.testing:
        # Criar diretório de logs se não existir
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        # Configurar arquivo de log rotativo
        file_handler = RotatingFileHandler(
            app.config.get('LOG_FILE', 'logs/app.log'),
            maxBytes=10240000,
            backupCount=10
        )
        
        # Formato do log
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        
        # Nível de log
        log_level = getattr(logging, app.config.get('LOG_LEVEL', 'INFO').upper())
        file_handler.setLevel(log_level)
        
        # Adicionar handler ao logger da aplicação
        app.logger.addHandler(file_handler)
        app.logger.setLevel(log_level)
        
        app.logger.info(f'{app.config.get("APP_NAME", "Move Marias")} startup')


def setup_jwt_handlers(app):
    """
    Configurar handlers personalizados para JWT.
    
    Args:
        app: Instância da aplicação Flask
    """
    from flask import jsonify
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        """Handler para token expirado."""
        return jsonify({
            'error': 'token_expired',
            'message': 'O token de acesso expirou. Por favor, faça login novamente.'
        }), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        """Handler para token inválido."""
        return jsonify({
            'error': 'token_invalid',
            'message': 'Token de acesso inválido.'
        }), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        """Handler para token ausente."""
        return jsonify({
            'error': 'token_missing',
            'message': 'Token de acesso é necessário para acessar este recurso.'
        }), 401
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        """Handler para token que precisa ser fresco."""
        return jsonify({
            'error': 'token_not_fresh',
            'message': 'Token fresco é necessário para esta operação.'
        }), 401
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        """Handler para token revogado."""
        return jsonify({
            'error': 'token_revoked',
            'message': 'O token foi revogado.'
        }), 401
    
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        """Definir identidade do usuário no JWT."""
        return user.id if hasattr(user, 'id') else user
    
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        """Carregar usuário pelo JWT."""
        from app.models.usuario import Usuario
        identity = jwt_data["sub"]
        return Usuario.query.filter_by(id=identity).one_or_none()
    
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        """Adicionar claims personalizados ao JWT."""
        from app.models.usuario import Usuario
        user = Usuario.query.get(identity)
        if user:
            return {
                'tipo_usuario': user.tipo_usuario.value if user.tipo_usuario else None,
                'nome': user.nome,
                'email': user.email,
                'ativo': user.ativo
            }
        return {}


def get_redis():
    """
    Obter instância do Redis.
    
    Returns:
        Redis: Cliente Redis configurado ou None se não disponível
    """
    try:
        return redis_client
    except:
        return None


def create_tables(app):
    """
    Criar todas as tabelas do banco de dados.
    
    Args:
        app: Instância da aplicação Flask
    """
    with app.app_context():
        # Importar todos os modelos para garantir que sejam registrados
        from app.models import usuario, beneficiaria
        from app.models.declaracao_comparecimento import DeclaracaoComparecimento
        from app.models.recibo_beneficio import ReciboBeneficio
        from app.models.anamnese_social import AnamneseSocial
        from app.models.membro_familiar import MembroFamiliar
        from app.models.ficha_evolucao import FichaEvolucao
        from app.models.termo_consentimento import TermoConsentimento
        
        # Criar todas as tabelas
        db.create_all()
        
        app.logger.info('Tabelas do banco de dados criadas com sucesso.')
