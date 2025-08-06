"""
Schemas para serialização/deserialização de usuários.

Este módulo contém os schemas Marshmallow para validação e
serialização dos dados de usuários.
"""

from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from app.models.usuario import TipoUsuarioEnum
from app.schemas.base import BaseSchema


class UsuarioSchema(BaseSchema):
    """Schema principal para usuário."""
    
    id = fields.UUID(dump_only=True, description="ID único do usuário")
    
    nome = fields.String(
        required=True,
        validate=validate.Length(min=2, max=200),
        description="Nome completo do usuário"
    )
    
    email = fields.Email(
        required=True,
        description="Email do usuário"
    )
    
    senha = fields.String(
        load_only=True,
        required=True,
        validate=validate.Length(min=6),
        description="Senha do usuário (mínimo 6 caracteres)"
    )
    
    tipo_usuario = fields.Enum(
        TipoUsuarioEnum,
        required=True,
        description="Tipo de usuário"
    )
    
    ativo = fields.Boolean(
        missing=True,
        description="Se o usuário está ativo"
    )
    
    ultimo_login = fields.DateTime(
        dump_only=True,
        format='iso',
        description="Data do último login"
    )
    
    criado_em = fields.DateTime(dump_only=True, format='iso')
    atualizado_em = fields.DateTime(dump_only=True, format='iso')


class LoginSchema(Schema):
    """Schema para login de usuário."""
    
    email = fields.Email(
        required=True,
        description="Email do usuário",
        error_messages={
            'required': 'Email é obrigatório',
            'invalid': 'Email deve ter um formato válido'
        }
    )
    
    senha = fields.String(
        required=True,
        description="Senha do usuário",
        error_messages={
            'required': 'Senha é obrigatória'
        }
    )


class TokenSchema(Schema):
    """Schema para resposta de tokens."""
    
    access_token = fields.String(description="Token de acesso")
    refresh_token = fields.String(description="Token de refresh")
    token_type = fields.String(description="Tipo do token")
    user = fields.Nested(UsuarioSchema, description="Dados do usuário")


class UsuarioCreateSchema(UsuarioSchema):
    """Schema para criação de usuário."""
    
    class Meta:
        exclude = ('id', 'ultimo_login', 'criado_em', 'atualizado_em')


class UsuarioUpdateSchema(UsuarioSchema):
    """Schema para atualização de usuário."""
    
    # Todos os campos são opcionais na atualização
    nome = fields.String(allow_none=True, validate=validate.Length(min=2, max=200))
    email = fields.Email(allow_none=True)
    senha = fields.String(load_only=True, allow_none=True, validate=validate.Length(min=6))
    tipo_usuario = fields.Enum(TipoUsuarioEnum, allow_none=True)
    ativo = fields.Boolean(allow_none=True)
    
    class Meta:
        exclude = ('id', 'ultimo_login', 'criado_em', 'atualizado_em')


# Instâncias dos schemas
usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)
usuario_create_schema = UsuarioCreateSchema()
usuario_update_schema = UsuarioUpdateSchema()
login_schema = LoginSchema()
token_schema = TokenSchema()
