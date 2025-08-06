"""
Aplicação Move Marias - Sistema de Gestão de Beneficiárias.

Este pacote contém toda a lógica da aplicação Flask, incluindo modelos,
rotas, schemas e serviços.
"""

from flask import Flask
from app.config import get_config
from app.extensions import init_extensions, create_tables
from app.utils.error_handlers import register_error_handlers

__version__ = '1.0.0'
__author__ = 'Equipe Move Marias'


def create_app(config_name=None):
    """
    Factory para criar instância da aplicação Flask.
    
    Args:
        config_name (str): Nome da configuração a usar
        
    Returns:
        Flask: Instância configurada da aplicação
    """
    app = Flask(__name__)
    
    # Carregar configuração
    if config_name:
        from app.config import config_by_name
        app.config.from_object(config_by_name[config_name])
    else:
        app.config.from_object(get_config())
    
    # Inicializar extensões
    init_extensions(app)
    
    # Registrar blueprints
    register_blueprints(app)
    
    # Registrar handlers de erro
    register_error_handlers(app)
    
    # Criar tabelas se necessário
    if app.config.get('SEED_DATABASE', False):
        create_tables(app)
        seed_initial_data(app)
    
    return app


def register_blueprints(app):
    """
    Registrar todos os blueprints da aplicação.
    
    Args:
        app: Instância da aplicação Flask
    """
    from app.routes.health import health_bp
    from app.routes.auth import auth_bp
    
    # Registrar blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp, url_prefix='/api/auth')


def seed_initial_data(app):
    """
    Popular dados iniciais no banco de dados.
    
    Args:
        app: Instância da aplicação Flask
    """
    with app.app_context():
        from app.models.usuario import Usuario, TipoUsuario
        from app.extensions import db, bcrypt
        
        # Verificar se já existem usuários
        if Usuario.query.count() == 0:
            # Criar usuário administrador
            admin = Usuario(
                nome='Administrador',
                email=app.config.get('DEFAULT_ADMIN_EMAIL', 'admin@movemarias.dev'),
                tipo_usuario=TipoUsuario.ADMINISTRADOR,
                ativo=True
            )
            admin.set_password(app.config.get('DEFAULT_ADMIN_PASSWORD', 'admin123'))
            
            # Criar usuário profissional
            prof = Usuario(
                nome='Profissional',
                email=app.config.get('DEFAULT_PROF_EMAIL', 'profissional@movemarias.dev'),
                tipo_usuario=TipoUsuario.PROFISSIONAL,
                ativo=True
            )
            prof.set_password(app.config.get('DEFAULT_PROF_PASSWORD', 'prof123'))
            
            # Salvar no banco
            db.session.add(admin)
            db.session.add(prof)
            db.session.commit()
            
            app.logger.info('Dados iniciais criados com sucesso.')


# Exportar função principal
__all__ = ['create_app']
