"""
Script para inicializar dados no banco de dados.

Este script cria usuários padrão e dados de exemplo para desenvolvimento.
"""

import os
from datetime import date, datetime
from flask import current_app

from app import create_app
from app.extensions import db
from app.models.usuario import Usuario, TipoUsuarioEnum
from app.models.beneficiaria import Beneficiaria


def create_default_users():
    """Criar usuários padrão do sistema."""
    print("Criando usuários padrão...")
    
    # Administrador padrão
    admin_email = current_app.config.get('DEFAULT_ADMIN_EMAIL', 'admin@movemarias.dev')
    admin_password = current_app.config.get('DEFAULT_ADMIN_PASSWORD', 'admin123')
    
    admin = Usuario.find_by_email(admin_email)
    if not admin:
        admin = Usuario(
            nome='Administrador do Sistema',
            email=admin_email,
            senha=admin_password,
            tipo_usuario=TipoUsuarioEnum.ADMIN
        )
        db.session.add(admin)
        print(f"Usuário administrador criado: {admin_email}")
    else:
        print(f"Usuário administrador já existe: {admin_email}")
    
    # Profissional padrão
    prof_email = current_app.config.get('DEFAULT_PROF_EMAIL', 'profissional@movemarias.dev')
    prof_password = current_app.config.get('DEFAULT_PROF_PASSWORD', 'prof123')
    
    profissional = Usuario.find_by_email(prof_email)
    if not profissional:
        profissional = Usuario(
            nome='Maria Silva',
            email=prof_email,
            senha=prof_password,
            tipo_usuario=TipoUsuarioEnum.PROFISSIONAL
        )
        db.session.add(profissional)
        print(f"Usuário profissional criado: {prof_email}")
    else:
        print(f"Usuário profissional já existe: {prof_email}")


def create_sample_beneficiarias():
    """Criar beneficiárias de exemplo."""
    print("Criando beneficiárias de exemplo...")
    
    beneficiarias_exemplo = [
        {
            'nome_completo': 'Ana Santos Silva',
            'cpf': '12345678901',
            'data_nascimento': date(1985, 3, 15),
            'contato1': '(11) 98765-4321',
            'endereco': 'Rua das Flores, 123',
            'bairro': 'Centro',
            'programa_servico': 'Oficina de Costura',
            'referencia': 'CRAS Central'
        },
        {
            'nome_completo': 'Beatriz Oliveira Costa',
            'cpf': '98765432109',
            'data_nascimento': date(1992, 7, 22),
            'contato1': '(11) 91234-5678',
            'endereco': 'Avenida Principal, 456',
            'bairro': 'Vila Nova',
            'programa_servico': 'Curso de Informática',
            'referencia': 'Indicação'
        },
        {
            'nome_completo': 'Carla Fernandes Lima',
            'cpf': '45678912301',
            'data_nascimento': date(1988, 11, 8),
            'contato1': '(11) 95555-1234',
            'endereco': 'Travessa da Paz, 789',
            'bairro': 'Jardim das Rosas',
            'programa_servico': 'Grupo de Apoio',
            'referencia': 'UBS do bairro'
        }
    ]
    
    for beneficiaria_data in beneficiarias_exemplo:
        # Verificar se já existe
        existing = Beneficiaria.find_by_cpf(beneficiaria_data['cpf'])
        if not existing:
            beneficiaria = Beneficiaria(**beneficiaria_data)
            db.session.add(beneficiaria)
            print(f"Beneficiária criada: {beneficiaria_data['nome_completo']}")
        else:
            print(f"Beneficiária já existe: {beneficiaria_data['nome_completo']}")


def seed_database():
    """
    Executar seed completo do banco de dados.
    """
    print("Iniciando seed do banco de dados...")
    
    try:
        # Criar usuários padrão
        create_default_users()
        
        # Criar beneficiárias de exemplo (apenas em desenvolvimento)
        if current_app.config.get('SEED_DATABASE', False):
            create_sample_beneficiarias()
        
        # Commit das alterações
        db.session.commit()
        print("Seed do banco de dados concluído com sucesso!")
        
    except Exception as e:
        db.session.rollback()
        print(f"Erro durante o seed: {e}")
        raise


def init_database():
    """
    Inicializar banco de dados (criar tabelas e seed).
    """
    print("Inicializando banco de dados...")
    
    # Criar tabelas
    try:
        db.create_all()
        print("Tabelas criadas com sucesso!")
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")
        raise
    
    # Executar seed
    seed_database()


if __name__ == '__main__':
    # Criar aplicação
    app = create_app('development')
    
    with app.app_context():
        init_database()
