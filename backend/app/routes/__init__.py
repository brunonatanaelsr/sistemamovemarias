"""
Módulo de rotas da aplicação.

Este módulo centraliza o registro de todas as rotas/blueprints
da aplicação Flask.
"""

from flask import Flask

from .health import health_bp
from .auth import auth_bp


def register_routes(app: Flask):
    """
    Registra todos os blueprints na aplicação Flask.
    
    Args:
        app: Instância da aplicação Flask
    """
    # Rota de health check (sem prefixo)
    app.register_blueprint(health_bp)
    
    # Rotas de autenticação
    app.register_blueprint(auth_bp)
    
    # TODO: Adicionar outras rotas quando criadas
    # from .usuarios import usuarios_bp
    # from .beneficiarias import beneficiarias_bp
    # from .formularios import formularios_bp
    # app.register_blueprint(usuarios_bp)
    # app.register_blueprint(beneficiarias_bp)
    # app.register_blueprint(formularios_bp)
