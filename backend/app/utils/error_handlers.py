"""
Handlers para tratamento de erros da aplicação.

Este módulo define os handlers para diferentes tipos de erros
que podem ocorrer na aplicação Flask.
"""

from flask import jsonify, request
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError, OperationalError
from marshmallow import ValidationError
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

from app.utils.logger import log_error, log_security_event


def register_error_handlers(app):
    """
    Registrar handlers de erro na aplicação.
    
    Args:
        app (Flask): Instância da aplicação Flask
    """
    
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        """Handler para erros de validação do Marshmallow."""
        return jsonify({
            'error': 'Dados inválidos',
            'message': 'Os dados enviados contêm erros de validação',
            'details': error.messages
        }), 400
    
    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):
        """Handler para erros de integridade do banco de dados."""
        # Log do erro
        log_error(error, context={'endpoint': request.endpoint})
        
        # Verificar tipo específico de erro
        error_message = str(error.orig)
        
        if 'unique constraint' in error_message.lower():
            return jsonify({
                'error': 'Dados duplicados',
                'message': 'Já existe um registro com estes dados'
            }), 409
        elif 'foreign key constraint' in error_message.lower():
            return jsonify({
                'error': 'Referência inválida',
                'message': 'Existe uma referência inválida nos dados'
            }), 400
        else:
            return jsonify({
                'error': 'Erro de integridade',
                'message': 'Erro ao processar os dados'
            }), 400
    
    @app.errorhandler(OperationalError)
    def handle_operational_error(error):
        """Handler para erros operacionais do banco de dados."""
        log_error(error, context={'endpoint': request.endpoint})
        
        return jsonify({
            'error': 'Erro de banco de dados',
            'message': 'Erro temporário no banco de dados. Tente novamente.'
        }), 503
    
    @app.errorhandler(InvalidTokenError)
    def handle_invalid_token_error(error):
        """Handler para erros de token JWT inválido."""
        log_security_event(
            'INVALID_TOKEN_ATTEMPT',
            {'error': str(error)},
            ip_address=request.remote_addr
        )
        
        return jsonify({
            'error': 'Token inválido',
            'message': 'Token de acesso inválido'
        }), 401
    
    @app.errorhandler(ExpiredSignatureError)
    def handle_expired_token_error(error):
        """Handler para erros de token JWT expirado."""
        return jsonify({
            'error': 'Token expirado',
            'message': 'Token de acesso expirado'
        }), 401
    
    @app.errorhandler(400)
    def handle_bad_request(error):
        """Handler para Bad Request (400)."""
        return jsonify({
            'error': 'Requisição inválida',
            'message': 'A requisição contém dados inválidos'
        }), 400
    
    @app.errorhandler(401)
    def handle_unauthorized(error):
        """Handler para Unauthorized (401)."""
        return jsonify({
            'error': 'Não autorizado',
            'message': 'Acesso não autorizado. Faça login para continuar.'
        }), 401
    
    @app.errorhandler(403)
    def handle_forbidden(error):
        """Handler para Forbidden (403)."""
        return jsonify({
            'error': 'Acesso negado',
            'message': 'Você não tem permissão para acessar este recurso'
        }), 403
    
    @app.errorhandler(404)
    def handle_not_found(error):
        """Handler para Not Found (404)."""
        return jsonify({
            'error': 'Não encontrado',
            'message': 'O recurso solicitado não foi encontrado'
        }), 404
    
    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        """Handler para Method Not Allowed (405)."""
        return jsonify({
            'error': 'Método não permitido',
            'message': 'Método HTTP não permitido para este endpoint'
        }), 405
    
    @app.errorhandler(409)
    def handle_conflict(error):
        """Handler para Conflict (409)."""
        return jsonify({
            'error': 'Conflito',
            'message': 'Conflito com o estado atual do recurso'
        }), 409
    
    @app.errorhandler(413)
    def handle_payload_too_large(error):
        """Handler para Payload Too Large (413)."""
        return jsonify({
            'error': 'Arquivo muito grande',
            'message': 'O arquivo enviado é muito grande'
        }), 413
    
    @app.errorhandler(415)
    def handle_unsupported_media_type(error):
        """Handler para Unsupported Media Type (415)."""
        return jsonify({
            'error': 'Tipo de arquivo não suportado',
            'message': 'O tipo de arquivo enviado não é suportado'
        }), 415
    
    @app.errorhandler(422)
    def handle_unprocessable_entity(error):
        """Handler para Unprocessable Entity (422)."""
        return jsonify({
            'error': 'Dados não processáveis',
            'message': 'Os dados enviados não podem ser processados'
        }), 422
    
    @app.errorhandler(429)
    def handle_rate_limit_exceeded(error):
        """Handler para Rate Limit Exceeded (429)."""
        log_security_event(
            'RATE_LIMIT_EXCEEDED',
            {'endpoint': request.endpoint},
            ip_address=request.remote_addr
        )
        
        return jsonify({
            'error': 'Limite de requisições excedido',
            'message': 'Muitas requisições. Tente novamente mais tarde.'
        }), 429
    
    @app.errorhandler(500)
    def handle_internal_server_error(error):
        """Handler para Internal Server Error (500)."""
        log_error(
            error,
            context={
                'endpoint': request.endpoint,
                'method': request.method,
                'url': request.url
            }
        )
        
        return jsonify({
            'error': 'Erro interno do servidor',
            'message': 'Ocorreu um erro interno. Tente novamente mais tarde.'
        }), 500
    
    @app.errorhandler(503)
    def handle_service_unavailable(error):
        """Handler para Service Unavailable (503)."""
        return jsonify({
            'error': 'Serviço indisponível',
            'message': 'Serviço temporariamente indisponível'
        }), 503
    
    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        """Handler genérico para exceções não tratadas."""
        log_error(
            error,
            context={
                'endpoint': request.endpoint,
                'method': request.method,
                'url': request.url
            }
        )
        
        # Em produção, não expor detalhes do erro
        if app.config.get('DEBUG', False):
            return jsonify({
                'error': 'Erro interno',
                'message': str(error),
                'type': type(error).__name__
            }), 500
        else:
            return jsonify({
                'error': 'Erro interno do servidor',
                'message': 'Ocorreu um erro interno. Tente novamente mais tarde.'
            }), 500


class APIException(Exception):
    """
    Exceção customizada para erros da API.
    
    Permite definir códigos de status HTTP e mensagens específicas.
    """
    
    def __init__(self, message, status_code=400, payload=None):
        """
        Inicializar exceção da API.
        
        Args:
            message (str): Mensagem de erro
            status_code (int): Código de status HTTP
            payload (dict, optional): Dados adicionais do erro
        """
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload
    
    def to_dict(self):
        """
        Converter exceção para dicionário.
        
        Returns:
            dict: Dados da exceção
        """
        result = {'error': self.message}
        if self.payload:
            result.update(self.payload)
        return result


class ValidationException(APIException):
    """Exceção para erros de validação."""
    
    def __init__(self, message, errors=None):
        super().__init__(message, status_code=400, payload={'errors': errors})


class AuthenticationException(APIException):
    """Exceção para erros de autenticação."""
    
    def __init__(self, message='Credenciais inválidas'):
        super().__init__(message, status_code=401)


class AuthorizationException(APIException):
    """Exceção para erros de autorização."""
    
    def __init__(self, message='Acesso negado'):
        super().__init__(message, status_code=403)


class NotFoundException(APIException):
    """Exceção para recursos não encontrados."""
    
    def __init__(self, message='Recurso não encontrado'):
        super().__init__(message, status_code=404)


class ConflictException(APIException):
    """Exceção para conflitos de dados."""
    
    def __init__(self, message='Conflito de dados'):
        super().__init__(message, status_code=409)


class BusinessRuleException(APIException):
    """Exceção para violações de regras de negócio."""
    
    def __init__(self, message):
        super().__init__(message, status_code=422)
