"""
Schemas para serialização/deserialização de Recibo de Benefício.

Este módulo contém os schemas Marshmallow para validação e
serialização dos dados de recibos de benefício.
"""

from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from datetime import datetime
from decimal import Decimal

from app.schemas.base import BaseSchema


class ReciboBeneficioSchema(BaseSchema):
    """Schema para Recibo de Benefício."""
    
    # Identificação
    id = fields.UUID(dump_only=True, description="ID único do recibo")
    
    # Relacionamentos
    beneficiaria_id = fields.UUID(
        required=True,
        description="ID da beneficiária",
        error_messages={
            'required': 'ID da beneficiária é obrigatório',
            'invalid': 'ID da beneficiária deve ser um UUID válido'
        }
    )
    
    # Dados do benefício
    tipo_beneficio = fields.String(
        required=True,
        validate=validate.Length(min=2, max=200),
        description="Tipo de benefício recebido",
        error_messages={
            'required': 'Tipo de benefício é obrigatório',
            'invalid': 'Tipo deve ter entre 2 e 200 caracteres'
        }
    )
    
    descricao_beneficio = fields.String(
        allow_none=True,
        validate=validate.Length(max=1000),
        description="Descrição detalhada do benefício"
    )
    
    valor_beneficio = fields.Decimal(
        allow_none=True,
        places=2,
        description="Valor monetário do benefício",
        validate=validate.Range(min=0),
        error_messages={
            'invalid': 'Valor deve ser um número decimal positivo'
        }
    )
    
    quantidade = fields.String(
        allow_none=True,
        validate=validate.Length(max=50),
        description="Quantidade de itens do benefício"
    )
    
    data_recebimento = fields.DateTime(
        required=True,
        format='%Y-%m-%d',
        description="Data de recebimento do benefício",
        error_messages={
            'required': 'Data de recebimento é obrigatória',
            'invalid': 'Data deve estar no formato YYYY-MM-DD'
        }
    )
    
    # Informações adicionais
    origem_beneficio = fields.String(
        allow_none=True,
        validate=validate.Length(max=200),
        description="Origem/fonte do benefício"
    )
    
    responsavel_entrega = fields.String(
        required=True,
        validate=validate.Length(min=2, max=200),
        description="Responsável pela entrega",
        error_messages={
            'required': 'Responsável pela entrega é obrigatório',
            'invalid': 'Nome deve ter entre 2 e 200 caracteres'
        }
    )
    
    observacoes = fields.String(
        allow_none=True,
        validate=validate.Length(max=1000),
        description="Observações sobre o benefício"
    )
    
    # Status e controle
    status = fields.String(
        validate=validate.OneOf(['entregue', 'pendente', 'cancelado']),
        missing='entregue',
        description="Status do benefício"
    )
    
    numero_recibo = fields.String(
        dump_only=True,
        description="Número sequencial do recibo"
    )
    
    # Auditoria
    criado_em = fields.DateTime(dump_only=True, format='iso')
    atualizado_em = fields.DateTime(dump_only=True, format='iso')
    
    @validates_schema
    def validate_data_recebimento(self, data, **kwargs):
        """Valida se a data de recebimento não é futura."""
        data_recebimento = data.get('data_recebimento')
        
        if data_recebimento and data_recebimento.date() > datetime.now().date():
            raise ValidationError(
                'Data de recebimento não pode ser futura',
                field_name='data_recebimento'
            )
    
    @validates_schema
    def validate_valor_quantidade(self, data, **kwargs):
        """Valida se pelo menos valor ou quantidade foi informado."""
        valor = data.get('valor_beneficio')
        quantidade = data.get('quantidade')
        
        if not valor and not quantidade:
            raise ValidationError(
                'É necessário informar pelo menos o valor ou a quantidade do benefício'
            )


class ReciboBeneficioCreateSchema(ReciboBeneficioSchema):
    """Schema para criação de recibo de benefício."""
    
    class Meta:
        exclude = ('id', 'numero_recibo', 'criado_em', 'atualizado_em')


class ReciboBeneficioUpdateSchema(ReciboBeneficioSchema):
    """Schema para atualização de recibo de benefício."""
    
    # Todos os campos são opcionais na atualização
    beneficiaria_id = fields.UUID(allow_none=True)
    tipo_beneficio = fields.String(
        allow_none=True,
        validate=validate.Length(min=2, max=200)
    )
    data_recebimento = fields.DateTime(allow_none=True, format='%Y-%m-%d')
    responsavel_entrega = fields.String(
        allow_none=True,
        validate=validate.Length(min=2, max=200)
    )
    
    class Meta:
        exclude = ('id', 'numero_recibo', 'criado_em', 'atualizado_em')


class ReciboBeneficioListSchema(Schema):
    """Schema para listagem de recibos de benefício."""
    
    id = fields.UUID(description="ID único do recibo")
    beneficiaria_id = fields.UUID(description="ID da beneficiária")
    beneficiaria_nome = fields.String(description="Nome da beneficiária")
    tipo_beneficio = fields.String()
    valor_beneficio = fields.Decimal(places=2, allow_none=True)
    quantidade = fields.String(allow_none=True)
    data_recebimento = fields.DateTime(format='%Y-%m-%d')
    responsavel_entrega = fields.String()
    status = fields.String()
    numero_recibo = fields.String(allow_none=True)
    criado_em = fields.DateTime(format='iso')


class ReciboBeneficioReportSchema(Schema):
    """Schema para relatórios de recibos de benefício."""
    
    # Dados da beneficiária
    beneficiaria_nome = fields.String()
    beneficiaria_cpf = fields.String()
    
    # Dados do recibo
    numero_recibo = fields.String(allow_none=True)
    tipo_beneficio = fields.String()
    descricao_beneficio = fields.String(allow_none=True)
    valor_beneficio = fields.Decimal(places=2, allow_none=True)
    quantidade = fields.String(allow_none=True)
    data_recebimento = fields.DateTime(format='%d/%m/%Y')
    origem_beneficio = fields.String(allow_none=True)
    responsavel_entrega = fields.String()
    status = fields.String()
    observacoes = fields.String(allow_none=True)
    
    # Auditoria
    criado_em = fields.DateTime(format='%d/%m/%Y %H:%M')


class ReciboBeneficioStatisticsSchema(Schema):
    """Schema para estatísticas de benefícios."""
    
    total_beneficios = fields.Integer(description="Total de benefícios")
    total_valor = fields.Decimal(places=2, description="Valor total dos benefícios")
    beneficios_por_tipo = fields.Dict(description="Benefícios agrupados por tipo")
    beneficios_por_mes = fields.Dict(description="Benefícios por mês")
    beneficiarias_atendidas = fields.Integer(description="Número de beneficiárias atendidas")


# Instâncias dos schemas para uso nas rotas
recibo_beneficio_schema = ReciboBeneficioSchema()
recibo_beneficio_create_schema = ReciboBeneficioCreateSchema()
recibo_beneficio_update_schema = ReciboBeneficioUpdateSchema()
recibo_beneficio_list_schema = ReciboBeneficioListSchema(many=True)
recibo_beneficio_report_schema = ReciboBeneficioReportSchema(many=True)
recibo_beneficio_statistics_schema = ReciboBeneficioStatisticsSchema()
