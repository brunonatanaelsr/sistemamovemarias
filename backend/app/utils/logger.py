"""
Configuração de logging da aplicação.

Este módulo configura o sistema de logs da aplicação Flask.
"""

import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime


def setup_logging(app):
    """
    Configurar sistema de logging da aplicação.
    
    Args:
        app (Flask): Instância da aplicação Flask
    """
    # Obter configurações de log
    log_level = getattr(logging, app.config.get('LOG_LEVEL', 'INFO'))
    log_file = app.config.get('LOG_FILE', 'logs/app.log')
    
    # Criar diretório de logs se não existir
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Configurar formato dos logs
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    
    # Configurar handler para arquivo
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10240000,  # 10MB
        backupCount=10
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)
    
    # Configurar handler para console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)
    
    # Configurar logger da aplicação
    app.logger.setLevel(log_level)
    app.logger.addHandler(file_handler)
    
    # Adicionar console handler apenas em desenvolvimento
    if app.config.get('DEBUG', False):
        app.logger.addHandler(console_handler)
    
    # Configurar loggers de bibliotecas externas
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    
    app.logger.info('Sistema de logging configurado')


def log_user_action(user_id, action, details=None):
    """
    Registrar ação do usuário.
    
    Args:
        user_id (str): ID do usuário
        action (str): Ação realizada
        details (dict, optional): Detalhes adicionais da ação
    """
    from flask import current_app
    
    log_entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'user_id': str(user_id),
        'action': action,
        'details': details or {}
    }
    
    current_app.logger.info(f"USER_ACTION: {log_entry}")


def log_api_request(endpoint, method, user_id=None, ip_address=None):
    """
    Registrar requisição da API.
    
    Args:
        endpoint (str): Endpoint da API
        method (str): Método HTTP
        user_id (str, optional): ID do usuário
        ip_address (str, optional): Endereço IP
    """
    from flask import current_app
    
    log_entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'endpoint': endpoint,
        'method': method,
        'user_id': str(user_id) if user_id else None,
        'ip_address': ip_address
    }
    
    current_app.logger.info(f"API_REQUEST: {log_entry}")


def log_security_event(event_type, details, user_id=None, ip_address=None):
    """
    Registrar evento de segurança.
    
    Args:
        event_type (str): Tipo do evento (LOGIN_FAILED, ACCOUNT_LOCKED, etc.)
        details (dict): Detalhes do evento
        user_id (str, optional): ID do usuário
        ip_address (str, optional): Endereço IP
    """
    from flask import current_app
    
    log_entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'event_type': event_type,
        'user_id': str(user_id) if user_id else None,
        'ip_address': ip_address,
        'details': details
    }
    
    current_app.logger.warning(f"SECURITY_EVENT: {log_entry}")


def log_data_access(data_type, record_id, action, user_id):
    """
    Registrar acesso a dados (LGPD compliance).
    
    Args:
        data_type (str): Tipo de dado acessado
        record_id (str): ID do registro
        action (str): Ação realizada (CREATE, READ, UPDATE, DELETE)
        user_id (str): ID do usuário
    """
    from flask import current_app
    
    log_entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'data_type': data_type,
        'record_id': str(record_id),
        'action': action,
        'user_id': str(user_id)
    }
    
    current_app.logger.info(f"DATA_ACCESS: {log_entry}")


def log_error(error, context=None, user_id=None):
    """
    Registrar erro da aplicação.
    
    Args:
        error (Exception): Erro ocorrido
        context (dict, optional): Contexto adicional
        user_id (str, optional): ID do usuário
    """
    from flask import current_app
    
    log_entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'error_type': type(error).__name__,
        'error_message': str(error),
        'user_id': str(user_id) if user_id else None,
        'context': context or {}
    }
    
    current_app.logger.error(f"APPLICATION_ERROR: {log_entry}")


class RequestLogger:
    """Middleware para logging de requisições."""
    
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Inicializar o middleware na aplicação."""
        app.before_request(self.log_request)
        app.after_request(self.log_response)
    
    def log_request(self):
        """Registrar dados da requisição."""
        from flask import request, g
        from flask_jwt_extended import get_jwt_identity
        
        g.start_time = datetime.utcnow()
        
        try:
            user_id = get_jwt_identity()
        except:
            user_id = None
        
        log_api_request(
            endpoint=request.endpoint,
            method=request.method,
            user_id=user_id,
            ip_address=request.remote_addr
        )
    
    def log_response(self, response):
        """Registrar dados da resposta."""
        from flask import g, current_app
        
        if hasattr(g, 'start_time'):
            duration = (datetime.utcnow() - g.start_time).total_seconds()
            
            if duration > 1.0:  # Log apenas requisições demoradas
                current_app.logger.warning(
                    f"SLOW_REQUEST: {duration:.2f}s - {response.status_code}"
                )
        
        return response
