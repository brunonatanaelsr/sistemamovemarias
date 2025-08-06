"""
Modelo de usuário do sistema.

Este módulo define o modelo SQLAlchemy para os usuários do sistema,
incluindo profissionais e administradores.
"""

import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime, Enum as SQLEnum
from flask_bcrypt import check_password_hash

from app.extensions import db, bcrypt


class TipoUsuarioEnum(Enum):
    """Enum para tipos de usuário."""
    ADMIN = 'admin'
    PROFISSIONAL = 'profissional'


class Usuario(db.Model):
    """
    Modelo para usuários do sistema.
    
    Representa profissionais e administradores que podem acessar o sistema.
    """
    
    __tablename__ = 'usuarios'
    
    # Campos principais
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    
    nome = Column(
        String(255),
        nullable=False,
        comment='Nome completo do usuário'
    )
    
    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
        comment='Email do usuário (usado para login)'
    )
    
    senha_hash = Column(
        String(255),
        nullable=False,
        comment='Hash da senha do usuário'
    )
    
    tipo_usuario = Column(
        SQLEnum(TipoUsuarioEnum),
        nullable=False,
        default=TipoUsuarioEnum.PROFISSIONAL,
        comment='Tipo de usuário (admin ou profissional)'
    )
    
    ativo = Column(
        db.Boolean,
        default=True,
        nullable=False,
        comment='Indica se o usuário está ativo no sistema'
    )
    
    # Campos de auditoria
    data_criacao = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        comment='Data e hora de criação do registro'
    )
    
    data_atualizacao = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        comment='Data e hora da última atualização'
    )
    
    ultimo_login = Column(
        DateTime,
        comment='Data e hora do último login'
    )
    
    tentativas_login = Column(
        db.Integer,
        default=0,
        comment='Número de tentativas de login falhadas'
    )
    
    bloqueado_ate = Column(
        DateTime,
        comment='Data até quando o usuário está bloqueado'
    )
    
    # Relacionamentos
    # TODO: Adicionar relacionamentos com formulários criados/modificados
    
    def __init__(self, nome, email, senha, tipo_usuario=TipoUsuarioEnum.PROFISSIONAL):
        """
        Inicializar novo usuário.
        
        Args:
            nome (str): Nome completo do usuário
            email (str): Email do usuário
            senha (str): Senha em texto plano (será hasheada)
            tipo_usuario (TipoUsuarioEnum): Tipo do usuário
        """
        self.nome = nome
        self.email = email.lower().strip()
        self.set_password(senha)
        self.tipo_usuario = tipo_usuario
    
    def set_password(self, senha):
        """
        Definir senha do usuário (com hash).
        
        Args:
            senha (str): Senha em texto plano
        """
        self.senha_hash = bcrypt.generate_password_hash(senha).decode('utf-8')
    
    def check_password(self, senha):
        """
        Verificar se a senha está correta.
        
        Args:
            senha (str): Senha em texto plano para verificar
            
        Returns:
            bool: True se a senha estiver correta, False caso contrário
        """
        return bcrypt.check_password_hash(self.senha_hash, senha)
    
    def is_admin(self):
        """
        Verificar se o usuário é administrador.
        
        Returns:
            bool: True se for administrador, False caso contrário
        """
        return self.tipo_usuario == TipoUsuarioEnum.ADMIN
    
    def is_profissional(self):
        """
        Verificar se o usuário é profissional.
        
        Returns:
            bool: True se for profissional, False caso contrário
        """
        return self.tipo_usuario == TipoUsuarioEnum.PROFISSIONAL
    
    def is_active(self):
        """
        Verificar se o usuário está ativo.
        
        Returns:
            bool: True se estiver ativo, False caso contrário
        """
        return self.ativo
    
    def is_blocked(self):
        """
        Verificar se o usuário está bloqueado.
        
        Returns:
            bool: True se estiver bloqueado, False caso contrário
        """
        if self.bloqueado_ate is None:
            return False
        return datetime.utcnow() < self.bloqueado_ate
    
    def increment_login_attempts(self):
        """Incrementar contador de tentativas de login."""
        self.tentativas_login += 1
        
        # Bloquear usuário após muitas tentativas
        from app.config import Config
        max_attempts = getattr(Config, 'MAX_LOGIN_ATTEMPTS', 5)
        timeout_minutes = getattr(Config, 'LOGIN_ATTEMPT_TIMEOUT', 15)
        
        if self.tentativas_login >= max_attempts:
            from datetime import timedelta
            self.bloqueado_ate = datetime.utcnow() + timedelta(minutes=timeout_minutes)
    
    def reset_login_attempts(self):
        """Resetar contador de tentativas de login."""
        self.tentativas_login = 0
        self.bloqueado_ate = None
        self.ultimo_login = datetime.utcnow()
    
    def to_dict(self, include_sensitive=False):
        """
        Converter usuário para dicionário.
        
        Args:
            include_sensitive (bool): Se deve incluir dados sensíveis
            
        Returns:
            dict: Dados do usuário
        """
        data = {
            'id': str(self.id),
            'nome': self.nome,
            'email': self.email,
            'tipo_usuario': self.tipo_usuario.value,
            'ativo': self.ativo,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'data_atualizacao': self.data_atualizacao.isoformat() if self.data_atualizacao else None,
            'ultimo_login': self.ultimo_login.isoformat() if self.ultimo_login else None
        }
        
        if include_sensitive:
            data.update({
                'tentativas_login': self.tentativas_login,
                'bloqueado_ate': self.bloqueado_ate.isoformat() if self.bloqueado_ate else None
            })
        
        return data
    
    def __repr__(self):
        """Representação string do usuário."""
        return f'<Usuario {self.email} ({self.tipo_usuario.value})>'
    
    @classmethod
    def find_by_email(cls, email):
        """
        Buscar usuário por email.
        
        Args:
            email (str): Email do usuário
            
        Returns:
            Usuario: Usuário encontrado ou None
        """
        return cls.query.filter_by(email=email.lower().strip()).first()
    
    @classmethod
    def find_by_id(cls, user_id):
        """
        Buscar usuário por ID.
        
        Args:
            user_id (str|UUID): ID do usuário
            
        Returns:
            Usuario: Usuário encontrado ou None
        """
        if isinstance(user_id, str):
            try:
                user_id = uuid.UUID(user_id)
            except ValueError:
                return None
        
        return cls.query.filter_by(id=user_id).first()
    
    @classmethod
    def get_active_users(cls):
        """
        Obter todos os usuários ativos.
        
        Returns:
            list: Lista de usuários ativos
        """
        return cls.query.filter_by(ativo=True).all()
    
    @classmethod
    def get_admins(cls):
        """
        Obter todos os administradores.
        
        Returns:
            list: Lista de administradores
        """
        return cls.query.filter_by(tipo_usuario=TipoUsuarioEnum.ADMIN).all()
    
    @classmethod
    def get_profissionais(cls):
        """
        Obter todos os profissionais.
        
        Returns:
            list: Lista de profissionais
        """
        return cls.query.filter_by(tipo_usuario=TipoUsuarioEnum.PROFISSIONAL).all()
