#!/usr/bin/env python3
"""
Sistema Move Marias - Aplicação Principal

Sistema de gestão para organizações que atendem mulheres em situação
de vulnerabilidade social, com foco na Casa das Marias.

Este sistema oferece:
- Gestão de beneficiárias
- Controle de documentos e formulários
- Sistema de autenticação com JWT
- APIs RESTful completas
- Interface administrativa
"""

import os
import sys
import click
from pathlib import Path

# Adicionar o diretório raiz ao path para imports
sys.path.append(str(Path(__file__).parent))

from flask import Flask, jsonify
from app.config import get_config
from app.extensions import init_extensions, create_tables
from app.utils.error_handlers import register_error_handlers


def create_app(config_name=None):
    """
    Factory function para criar a aplicação Flask.
    
    Args:
        config_name (str): Nome do ambiente de configuração
        
    Returns:
        Flask: Instância configurada da aplicação
    """
    app = Flask(__name__)
    
    # Configuração
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    config_class = get_config()
    app.config.from_object(config_class)
    
    # Inicializar extensões
    init_extensions(app)
    
    # Registrar blueprints
    register_blueprints(app)
    
    # Registrar handlers de erro
    register_error_handlers(app)
    
    # Registrar comandos CLI
    register_cli_commands(app)
    
    # Criar tabelas do banco
    if app.config.get('SEED_DATABASE', False):
        create_tables(app)
        seed_initial_data(app)
    
    # Log de inicialização
    app.logger.info(f'Sistema Move Marias iniciado em modo {config_name}')
    
    return app


def register_blueprints(app):
    """
    Registrar todos os blueprints da aplicação.
    
    Args:
        app: Instância da aplicação Flask
    """
    # Importar blueprints
    from app.routes.health import health_bp
    from app.routes.auth import auth_bp
    
    # Registrar blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    # Blueprint principal para documentação da API
    @app.route('/')
    def index():
        """Endpoint raiz com informações da API."""
        return jsonify({
            'name': app.config.get('APP_NAME', 'Sistema Move Marias'),
            'version': app.config.get('APP_VERSION', '1.0.0'),
            'description': 'API para gestão de beneficiárias e documentos',
            'endpoints': {
                'health': '/health',
                'api_docs': '/api',
                'auth': '/api/auth',
                'beneficiarias': '/api/beneficiarias (em desenvolvimento)',
                'documentos': '/api/documentos (em desenvolvimento)'
            },
            'status': 'operational'
        })
    
    @app.route('/api')
    def api_info():
        """Informações detalhadas da API."""
        return jsonify({
            'api_version': 'v1',
            'authentication': 'JWT Bearer Token',
            'supported_methods': ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
            'content_type': 'application/json',
            'endpoints': {
                'auth': {
                    'login': 'POST /api/auth/login',
                    'logout': 'POST /api/auth/logout',
                    'refresh': 'POST /api/auth/refresh',
                    'change_password': 'POST /api/auth/change-password',
                    'verify': 'GET /api/auth/verify'
                },
                'beneficiarias': {
                    'list': 'GET /api/beneficiarias',
                    'create': 'POST /api/beneficiarias',
                    'get': 'GET /api/beneficiarias/<id>',
                    'update': 'PUT /api/beneficiarias/<id>',
                    'delete': 'DELETE /api/beneficiarias/<id>'
                }
            }
        })


def register_cli_commands(app):
    """
    Registrar comandos CLI personalizados.
    
    Args:
        app: Instância da aplicação Flask
    """
    @app.cli.command()
    def create_db():
        """Criar todas as tabelas do banco de dados."""
        create_tables(app)
        click.echo('Tabelas criadas com sucesso!')
    
    @app.cli.command()
    def seed_db():
        """Popular banco com dados iniciais."""
        seed_initial_data(app)
        click.echo('Dados iniciais inseridos com sucesso!')
    
    @app.cli.command()
    def create_admin():
        """Criar usuário administrador."""
        from app.models.usuario import Usuario, TipoUsuario
        from app.extensions import db
        
        email = app.config.get('DEFAULT_ADMIN_EMAIL')
        password = app.config.get('DEFAULT_ADMIN_PASSWORD')
        
        if Usuario.query.filter_by(email=email).first():
            click.echo(f'Usuário {email} já existe!')
            return
        
        admin = Usuario(
            nome='Administrador',
            email=email,
            tipo_usuario=TipoUsuario.ADMINISTRADOR,
            ativo=True
        )
        admin.set_password(password)
        
        db.session.add(admin)
        db.session.commit()
        
        click.echo(f'Administrador criado: {email}')


def seed_initial_data(app):
    """
    Popular banco com dados iniciais para desenvolvimento.
    
    Args:
        app: Instância da aplicação Flask
    """
    with app.app_context():
        from app.models.usuario import Usuario, TipoUsuario
        from app.extensions import db
        
        try:
            # Verificar se já existem usuários
            if Usuario.query.count() > 0:
                app.logger.info('Dados já existem, pulando seeding.')
                return
            
            # Criar usuário administrador
            admin = Usuario(
                nome='Administrador Sistema',
                email=app.config.get('DEFAULT_ADMIN_EMAIL'),
                tipo_usuario=TipoUsuario.ADMINISTRADOR,
                ativo=True
            )
            admin.set_password(app.config.get('DEFAULT_ADMIN_PASSWORD'))
            
            # Criar usuário profissional
            prof = Usuario(
                nome='Profissional Exemplo',
                email=app.config.get('DEFAULT_PROF_EMAIL'),
                tipo_usuario=TipoUsuario.PROFISSIONAL,
                ativo=True
            )
            prof.set_password(app.config.get('DEFAULT_PROF_PASSWORD'))
            
            # Salvar no banco
            db.session.add(admin)
            db.session.add(prof)
            db.session.commit()
            
            app.logger.info('Dados iniciais inseridos com sucesso!')
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f'Erro ao inserir dados iniciais: {str(e)}')


if __name__ == '__main__':
    """
    Executar aplicação em modo de desenvolvimento.
    
    Para produção, usar um servidor WSGI como Gunicorn:
    gunicorn -w 4 -b 0.0.0.0:5000 app:app
    """
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    app = create_app()
    app.run(
        host=host,
        port=port,
        debug=debug,
        threaded=True
    )
