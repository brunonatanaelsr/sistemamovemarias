"""
Rotas para autenticação de usuários.

Este módulo contém as rotas para login, logout, refresh de token
e gerenciamento de sessões de usuários.
"""

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import (
    jwt_required, 
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_jwt
)
from werkzeug.security import check_password_hash
from datetime import timedelta

from app.models.usuario import Usuario
from app.schemas.usuario import (
    login_schema,
    usuario_schema,
    token_schema
)
from app.utils.error_handlers import handle_validation_error, handle_not_found
from app.utils.logger import log_security_event

# Criar blueprint para autenticação
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Lista de tokens revogados (em produção usar Redis)
revoked_tokens = set()


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Autenticar usuário e gerar tokens de acesso.
    
    Body (JSON):
        email (str): Email do usuário
        senha (str): Senha do usuário
    
    Returns:
        JSON: Tokens de acesso e refresh + dados do usuário
    """
    try:
        # Validar dados de entrada
        data = login_schema.load(request.json)
    except Exception as e:
        return handle_validation_error(e)
    
    email = data['email']
    senha = data['senha']
    
    # Buscar usuário pelo email
    usuario = Usuario.find_by_email(email)
    
    if not usuario:
        log_security_event('login_failed', {'email': email, 'reason': 'user_not_found'})
        return jsonify({
            'success': False,
            'message': 'Email ou senha inválidos'
        }), 401
    
    # Verificar se usuário está ativo
    if not usuario.ativo:
        log_security_event('login_failed', {'email': email, 'reason': 'user_inactive'})
        return jsonify({
            'success': False,
            'message': 'Usuário inativo. Entre em contato com o administrador.'
        }), 401
    
    # Verificar senha
    if not usuario.check_password(senha):
        log_security_event('login_failed', {'email': email, 'reason': 'wrong_password'})
        return jsonify({
            'success': False,
            'message': 'Email ou senha inválidos'
        }), 401
    
    # Criar tokens
    access_token = create_access_token(
        identity=str(usuario.id),
        expires_delta=timedelta(hours=current_app.config.get('JWT_ACCESS_TOKEN_EXPIRES', 24))
    )
    
    refresh_token = create_refresh_token(
        identity=str(usuario.id),
        expires_delta=timedelta(days=current_app.config.get('JWT_REFRESH_TOKEN_EXPIRES', 30))
    )
    
    # Atualizar último login
    usuario.update_last_login()
    
    # Log de sucesso
    log_security_event('login_success', {
        'user_id': str(usuario.id),
        'email': email,
        'tipo_usuario': usuario.tipo_usuario.value
    })
    
    return jsonify({
        'success': True,
        'message': 'Login realizado com sucesso',
        'data': {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'Bearer',
            'user': usuario_schema.dump(usuario)
        }
    }), 200


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Renovar token de acesso usando refresh token.
    
    Headers:
        Authorization: Bearer <refresh_token>
    
    Returns:
        JSON: Novo token de acesso
    """
    # Verificar se token foi revogado
    jti = get_jwt()['jti']
    if jti in revoked_tokens:
        return jsonify({
            'success': False,
            'message': 'Token inválido'
        }), 401
    
    # Obter usuário atual
    current_user_id = get_jwt_identity()
    usuario = Usuario.find_by_id(current_user_id)
    
    if not usuario or not usuario.ativo:
        return jsonify({
            'success': False,
            'message': 'Usuário não encontrado ou inativo'
        }), 401
    
    # Criar novo token de acesso
    new_access_token = create_access_token(
        identity=current_user_id,
        expires_delta=timedelta(hours=current_app.config.get('JWT_ACCESS_TOKEN_EXPIRES', 24))
    )
    
    return jsonify({
        'success': True,
        'message': 'Token renovado com sucesso',
        'data': {
            'access_token': new_access_token,
            'token_type': 'Bearer'
        }
    }), 200


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Fazer logout do usuário (revogar token).
    
    Headers:
        Authorization: Bearer <access_token>
    
    Returns:
        JSON: Confirmação de logout
    """
    # Adicionar token à lista de revogados
    jti = get_jwt()['jti']
    revoked_tokens.add(jti)
    
    # Log de logout
    current_user_id = get_jwt_identity()
    log_security_event('logout', {'user_id': current_user_id})
    
    return jsonify({
        'success': True,
        'message': 'Logout realizado com sucesso'
    }), 200


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Obter dados do usuário atual.
    
    Headers:
        Authorization: Bearer <access_token>
    
    Returns:
        JSON: Dados do usuário logado
    """
    current_user_id = get_jwt_identity()
    usuario = Usuario.find_by_id(current_user_id)
    
    if not usuario:
        return handle_not_found('Usuário não encontrado')
    
    return jsonify({
        'success': True,
        'message': 'Dados do usuário obtidos com sucesso',
        'data': usuario_schema.dump(usuario)
    }), 200


@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """
    Alterar senha do usuário atual.
    
    Headers:
        Authorization: Bearer <access_token>
    
    Body (JSON):
        senha_atual (str): Senha atual
        nova_senha (str): Nova senha
        confirmar_senha (str): Confirmação da nova senha
    
    Returns:
        JSON: Confirmação de alteração
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Dados não fornecidos'
            }), 400
        
        senha_atual = data.get('senha_atual')
        nova_senha = data.get('nova_senha')
        confirmar_senha = data.get('confirmar_senha')
        
        # Validações básicas
        if not all([senha_atual, nova_senha, confirmar_senha]):
            return jsonify({
                'success': False,
                'message': 'Todos os campos são obrigatórios'
            }), 400
        
        if nova_senha != confirmar_senha:
            return jsonify({
                'success': False,
                'message': 'Nova senha e confirmação não coincidem'
            }), 400
        
        if len(nova_senha) < 6:
            return jsonify({
                'success': False,
                'message': 'Nova senha deve ter pelo menos 6 caracteres'
            }), 400
        
        # Obter usuário atual
        current_user_id = get_jwt_identity()
        usuario = Usuario.find_by_id(current_user_id)
        
        if not usuario:
            return handle_not_found('Usuário não encontrado')
        
        # Verificar senha atual
        if not usuario.check_password(senha_atual):
            return jsonify({
                'success': False,
                'message': 'Senha atual incorreta'
            }), 400
        
        # Atualizar senha
        usuario.set_password(nova_senha)
        usuario.save()
        
        # Log de alteração de senha
        log_security_event('password_changed', {'user_id': current_user_id})
        
        return jsonify({
            'success': True,
            'message': 'Senha alterada com sucesso'
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Erro ao alterar senha: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Erro interno do servidor'
        }), 500


@auth_bp.route('/verify-token', methods=['GET'])
@jwt_required()
def verify_token():
    """
    Verificar se token está válido.
    
    Headers:
        Authorization: Bearer <access_token>
    
    Returns:
        JSON: Status do token
    """
    return jsonify({
        'success': True,
        'message': 'Token válido',
        'data': {
            'user_id': get_jwt_identity(),
            'valid': True
        }
    }), 200


# Middleware para verificar tokens revogados
@auth_bp.before_app_request
def check_if_token_revoked():
    """Verifica se o token foi revogado."""
    if request.endpoint and 'auth' in request.endpoint:
        return
    
    try:
        jti = get_jwt().get('jti')
        if jti in revoked_tokens:
            return jsonify({
                'success': False,
                'message': 'Token foi revogado'
            }), 401
    except:
        # Se não há JWT no request, ignora
        pass
