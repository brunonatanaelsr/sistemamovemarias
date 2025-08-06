"""
Schema base para todos os schemas Marshmallow do sistema.

Este módulo contém o schema base que deve ser herdado por todos
os outros schemas para garantir consistência.
"""

from marshmallow import Schema, fields, post_load
from datetime import datetime


class BaseSchema(Schema):
    """Schema base com funcionalidades comuns."""
    
    # Campos padrão de auditoria
    criado_em = fields.DateTime(
        dump_only=True,
        format='iso',
        description="Data de criação do registro"
    )
    
    atualizado_em = fields.DateTime(
        dump_only=True,
        format='iso',
        description="Data da última atualização"
    )
    
    class Meta:
        """Configurações padrão do schema."""
        # Ordenar campos por ordem alfabética
        ordered = True
        # Incluir campos desconhecidos
        unknown = 'EXCLUDE'
        # Formato de data padrão
        dateformat = '%Y-%m-%d'
        datetimeformat = 'iso'
    
    @post_load
    def make_object(self, data, **kwargs):
        """Hook executado após carregamento dos dados."""
        # Remove valores None dos dados
        return {k: v for k, v in data.items() if v is not None}


class PaginationSchema(Schema):
    """Schema para metadados de paginação."""
    
    page = fields.Integer(
        description="Página atual",
        example=1
    )
    
    per_page = fields.Integer(
        description="Itens por página",
        example=20
    )
    
    total = fields.Integer(
        description="Total de itens",
        example=150
    )
    
    pages = fields.Integer(
        description="Total de páginas",
        example=8
    )
    
    has_prev = fields.Boolean(
        description="Tem página anterior",
        example=False
    )
    
    has_next = fields.Boolean(
        description="Tem próxima página",
        example=True
    )
    
    prev_num = fields.Integer(
        allow_none=True,
        description="Número da página anterior",
        example=None
    )
    
    next_num = fields.Integer(
        allow_none=True,
        description="Número da próxima página",
        example=2
    )


class ResponseSchema(Schema):
    """Schema padrão para respostas da API."""
    
    success = fields.Boolean(
        description="Sucesso da operação",
        example=True
    )
    
    message = fields.String(
        description="Mensagem de retorno",
        example="Operação realizada com sucesso"
    )
    
    data = fields.Raw(
        allow_none=True,
        description="Dados de retorno"
    )
    
    pagination = fields.Nested(
        PaginationSchema,
        allow_none=True,
        description="Metadados de paginação"
    )
    
    errors = fields.List(
        fields.String(),
        allow_none=True,
        description="Lista de erros",
        example=[]
    )


class ErrorSchema(Schema):
    """Schema para respostas de erro."""
    
    success = fields.Boolean(
        description="Sucesso da operação",
        example=False
    )
    
    message = fields.String(
        description="Mensagem de erro",
        example="Erro na validação dos dados"
    )
    
    errors = fields.Dict(
        description="Detalhes dos erros de validação",
        example={
            "campo": ["Mensagem de erro do campo"]
        }
    )
    
    code = fields.Integer(
        description="Código do erro HTTP",
        example=400
    )


# Instâncias dos schemas base
response_schema = ResponseSchema()
error_schema = ErrorSchema()
pagination_schema = PaginationSchema()
