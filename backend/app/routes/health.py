"""
Rotas de health check da aplicação.

Este módulo define rotas para verificação de saúde da aplicação
e monitoramento de status.
"""

from flask import Blueprint, jsonify
from datetime import datetime
import sys
import os

from app.extensions import db

health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
def health_check():
    """
    Endpoint de health check básico.
    
    Returns:
        JSON com status da aplicação
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })


@health_bp.route('/health/detailed', methods=['GET'])
def detailed_health_check():
    """
    Endpoint de health check detalhado.
    
    Returns:
        JSON com informações detalhadas da aplicação
    """
    # Verificar status do banco de dados
    db_status = 'healthy'
    try:
        # Executar query simples para testar conexão
        db.session.execute('SELECT 1')
        db.session.commit()
    except Exception as e:
        db_status = f'unhealthy: {str(e)}'
    
    # Informações do sistema
    system_info = {
        'python_version': sys.version,
        'platform': sys.platform,
        'process_id': os.getpid()
    }
    
    # Status geral
    overall_status = 'healthy' if db_status == 'healthy' else 'unhealthy'
    
    return jsonify({
        'status': overall_status,
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0',
        'checks': {
            'database': db_status,
            'system': system_info
        }
    })


@health_bp.route('/ready', methods=['GET'])
def readiness_check():
    """
    Endpoint de readiness check (para Kubernetes).
    
    Returns:
        JSON com status de prontidão da aplicação
    """
    try:
        # Verificar se o banco está acessível
        db.session.execute('SELECT 1')
        db.session.commit()
        
        return jsonify({
            'status': 'ready',
            'timestamp': datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'not ready',
            'timestamp': datetime.utcnow().isoformat(),
            'error': str(e)
        }), 503


@health_bp.route('/live', methods=['GET'])
def liveness_check():
    """
    Endpoint de liveness check (para Kubernetes).
    
    Returns:
        JSON com status de vida da aplicação
    """
    return jsonify({
        'status': 'alive',
        'timestamp': datetime.utcnow().isoformat()
    })


@health_bp.route('/metrics', methods=['GET'])
def metrics():
    """
    Endpoint básico de métricas.
    
    Returns:
        JSON com métricas básicas da aplicação
    """
    try:
        # Contar registros principais
        from app.models.usuario import Usuario
        from app.models.beneficiaria import Beneficiaria
        
        usuario_count = Usuario.query.filter_by(ativo=True).count()
        beneficiaria_count = Beneficiaria.query.filter_by(ativo=True).count()
        
        return jsonify({
            'timestamp': datetime.utcnow().isoformat(),
            'metrics': {
                'usuarios_ativos': usuario_count,
                'beneficiarias_ativas': beneficiaria_count
            }
        })
    except Exception as e:
        return jsonify({
            'timestamp': datetime.utcnow().isoformat(),
            'error': f'Erro ao obter métricas: {str(e)}'
        }), 500
